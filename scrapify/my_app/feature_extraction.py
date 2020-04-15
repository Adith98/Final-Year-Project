import pandas as pd
import spacy
import demoji
import pickle
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
    'cost': [0, 0, []],
    'quality': [0, 0, []],
    'battery': [0, 0, []],
    'display': [0, 0, []],
    'camera': [0, 0, []],
    'design': [0, 0, []],
    'performance': [0, 0, []]
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
              "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

nlp = spacy.load("en_core_web_lg")


def get_aspects(x):
    doc = nlp(x)  ## Tokenize and extract grammatical components
    doc = [i.text for i in doc if
           i.text not in stop_words and i.pos_ == "NOUN"]  ## Remove common words and retain only nouns
    doc = list(map(lambda i: i.lower(), doc))  ## Normalize text to lower case
    doc = pd.Series(doc)
    doc = doc.value_counts().head().index.tolist()  ## Get 5 most frequent nouns
    return doc


excel_name = "C:/Users/shetty/Desktop/adith/Practice/Django/scrapify/my_app/static/my_app/product_reviews/R_Samsung Galaxy 438356.xlsx"

df = pd.read_excel(excel_name)
Review = df['Review'].tolist()

for rev in Review:
    rev = demoji.replace(rev, "")
    aspects = get_aspects(rev)
    for key in features.keys():
        if any(item in features[key] for item in aspects):
            count[key][0] += 1
            count[key][2].append(rev)

for key in count:
    vector = vectorizer.transform(count[key][2])
    prediction_linear = classifier.predict(vector)
    avg = sum(prediction_linear) / len(prediction_linear)
    count[key][1] = avg
    print(str(key) + " : " + str(count[key][0]) + " : " + str(count[key][1]))
