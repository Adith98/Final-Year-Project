import pandas as pd
import time
from sklearn import svm
from sklearn.metrics import classification_report
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection

# train Data
trainData = pd.read_csv("Cell_Phones_and_Accessories_5.csv", nrows=200000)

# test Data
testData = pd.read_csv("Cell_Phones_and_Accessories_5.csv", skiprows=range(1, 200001), nrows=150000)


vectorizer = TfidfVectorizer(min_df=5,
                             max_df=0.8,
                             sublinear_tf=True,
                             use_idf=True, encoding='utf-8')

train_vectors = vectorizer.fit_transform(trainData['reviewText'].values.astype('U'))
print("done 1")
test_vectors = vectorizer.transform(testData['reviewText'].values.astype('U'))
print("done 2")
# Perform classification with SVM, kernel=linear
classifier_linear = svm.SVC(kernel='linear')
t0 = time.time()
classifier_linear.fit(train_vectors, trainData['overall'])
t1 = time.time()
prediction_linear = classifier_linear.predict(test_vectors)
t2 = time.time()
time_linear_train = t1 - t0
time_linear_predict = t2 - t1
# results
print("Training time: %fs; Prediction time: %fs" % (time_linear_train, time_linear_predict))
report = classification_report(testData['overall'], prediction_linear, output_dict=True)

print('1 ', report['1.0'])
print('2 ', report['2.0'])
print('3 ', report['3.0'])
print('4 ', report['4.0'])
print('5 ', report['5.0'])

# pickling the vectorizer
pickle.dump(vectorizer, open('vectorizer_cellphone.sav', 'wb'))
# pickling the model
pickle.dump(classifier_linear, open('classifier_cellphone.sav', 'wb'))

review = """this is a good product"""
review_vector = vectorizer.transform([review])  # vectorizing
print(classifier_linear.predict(review_vector))

