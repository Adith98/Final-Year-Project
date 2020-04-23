import pandas as pd
import spacy
import demoji
import pickle
import nltk
import time

vectorizer = pickle.load(open('vectorizer_cellphone.sav', 'rb'))
classifier = pickle.load(open('classifier_cellphone.sav', 'rb'))

features = {
    'cost': ['cost', 'money', 'price', 'cheap', 'expensive', 'costly', 'value', 'worth'],
    'quality': ['quality', 'durability', 'material', 'fitting', 'weight', 'balance', 'finish', 'damage'],
    'battery': ['battery', 'mah', 'charging', 'life', 'backup'],
    'display': ['display', 'screen', 'resolution'],
    'camera': ['camera', 'photo', 'selfie', 'mp', 'megapixel', 'flash'],
    'design': ['design', 'sleek', 'hefty', 'slim', 'lightweight', 'thick', 'look'],
    'performance': ['performance', 'slow', 'fast', 'speed', 'lag']
}
count = {
    'cost': [0, 0, [], 0],
    'quality': [0, 0, [], 0],
    'battery': [0, 0, [], 0],
    'display': [0, 0, [], 0],
    'camera': [0, 0, [], 0],
    'design': [0, 0, [], 0],
    'performance': [0, 0, [], 0]
}

product = {
    'review': [],
    'score': [],
    'aspects': []
}

stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
              "product",
              "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
              "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these",
              "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do",
              "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
              "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before",
              "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
              "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
              "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
              "too", "very", "can", "will", "just", "don", "should", "now"]

nlp = spacy.load("en_core_web_lg")
tokenizer = nltk.RegexpTokenizer(r"\w+")


def get_aspects(x):
    doc = tokenizer.tokenize(x)
    #doc = nlp(doc)

    #print(doc)
    doc = [i for i in doc if
           i not in stop_words and i]  ## Remove common words and retain only nouns
    #doc = list(map(lambda i: i.lower(), doc))  ## Normalize text to lower case
    #doc = pd.Series(doc)
    #doc = doc.value_counts().index.tolist()  ## Get 5 most frequent nouns
    return doc


excel_name = "C:/Users/shetty/Desktop/adith/Practice/Django/scrapify/my_app/static/my_app/product_reviews/R_Infinix S5 Pro 300205.xlsx"
df = pd.read_excel(excel_name)
#Review = df['Review'].to_list()
'''
for rev in Review:
    rev = demoji.replace(rev, "")
    aspects = get_aspects(rev)
    print(aspects)

    vector = vectorizer.transform([rev])
    prediction_linear = classifier.predict(vector)
    product['review'].append(rev)
    product['score'].append(prediction_linear[0])
    list1 = []

    for key in features.keys():
        if any(item in features[key] for item in aspects):
            count[key][0] += 1
            count[key][3] += prediction_linear[0]
            print(key)
            list1.append(key)
    product['aspects'].append(list1)


for key in count:
    if count[key][0] is not 0:
        avg = count[key][3] / count[key][0]
        count[key][1] = avg
    print(str(key) + " : " + str(count[key][0]) + " : " + str(count[key][1]))

'''
Review = df['Review'].to_list()
aspects_list = []
for i in range(len(df['Review'].to_list())):
    aspects = get_aspects(df["Review"][i])
    list1 = []
    for key in features.keys():
        if any(item in features[key] for item in aspects):
            count[key][0] += 1
            count[key][1] += df['Score'][i]
            list1.append(key)
    aspects_list.append(list1)

for key in count:
    if count[key][0] is not 0:
        avg = count[key][1] / count[key][0]
        count[key][2] = avg




print(count)


