import demoji
import pandas as pd
import pickle
import time
from sklearn.metrics import classification_report
from pandas import DataFrame
import csv


def test_preprocessing():
    excel_name = "C:/Users/shetty/Desktop/adith/Practice/Django/scrapify/my_app/static/my_app/product_reviews/R_Apple " \
                 "AirPods P72665.xlsx "
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


def clean_the_review(dirty_review):
    clean_review = demoji.replace(dirty_review, "")
    return clean_review
