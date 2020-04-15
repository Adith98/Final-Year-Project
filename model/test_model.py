import pandas as pd
import pickle
import time
from sklearn.metrics import classification_report
import nltk

excel_path = "sample.xlsx"
df = pd.read_excel(excel_path)
testData = pd.read_csv("Cell_Phones_and_Accessories_5.csv", nrows=300)

vectorizer = pickle.load(open('vectorizer_cellphone.sav', 'rb'))
classifier = pickle.load(open('classifier_cellphone.sav', 'rb'))

train_vectors = vectorizer.transform(testData['reviewText'].values.astype('U'))
prediction_linear = classifier.predict(train_vectors)
t2 = time.time()
avg = 0
pos = 0
neg = 0
neutral = 0
total = 0

for i in range(0, len(prediction_linear)):
    avg += prediction_linear[i]


print()
print("Prediction time: %fs" % (t2))
print()
avg /= len(prediction_linear)
print("rating:  %fs" % (avg))
print()
report = classification_report(testData['overall'], prediction_linear, output_dict=True)

print('1 ', report['1.0'], len([i for i in prediction_linear if i == 1.0]))
print('2 ', report['2.0'], len([i for i in prediction_linear if i == 2.0]))
print('3 ', report['3.0'], len([i for i in prediction_linear if i == 3.0]))
print('4 ', report['4.0'], len([i for i in prediction_linear if i == 4.0]))
print('5 ', report['5.0'], len([i for i in prediction_linear if i == 5.0]))




