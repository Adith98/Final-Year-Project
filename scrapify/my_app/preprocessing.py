import demoji
import pandas as pd
import pickle
import time
from sklearn.metrics import classification_report
from pandas import DataFrame
import csv

excel_name = "R_JVC MC210 80 W Bluetooth Party Speaker.xlsx"
df = pd.read_excel(excel_name)
Review = df['Review'].tolist()
cleaned_review = []

for review in Review:
    cleaned_review.append(demoji.replace(review, ""))

dic = {'Review': cleaned_review}
df1 = pd.DataFrame(dic)

df = df.assign(Review=df1['Review'])
print(df)

excel = df.to_excel('sample.xlsx')
