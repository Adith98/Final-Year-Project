import pandas as pd
import json
import gzip


def parse(path):
    g = gzip.open(path, 'rb')
    for l in g:
        yield json.loads(l)


def getDF(path):
    i = 0
    df = {}
    for d in parse(path):
        df[i] = d
        i += 1
    return pd.DataFrame.from_dict(df, orient='index')


df = getDF('Cell_Phones_and_Accessories_5.json.gz')

new = df[['reviewText', 'overall', 'verified']].copy()
new = new.dropna(how='all')
new.drop(new[new['verified'] == False].index, inplace=True)
print(new.describe(include='all'))
print(new.shape)

new_o = new[['reviewText', 'overall']].copy()
excel = new_o.to_csv('Cell_Phones_and_Accessories_5.csv', index=None, header=True)

print(new_o[:5])
