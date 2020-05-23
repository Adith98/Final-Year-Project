import importlib
import datetime
import os
from pandas import DataFrame
import requests
import time
from bs4 import BeautifulSoup as soup
import urllib.parse as urlparse
from urllib.request import urlopen as uReq
import demoji
import pickle
import spacy
import pandas as pd
import nltk

from celery import shared_task
from .backend import ProgressRecorder
from .models import Link


class WebScraping:
    def get_info_url(self, url):
        url = url
        url = WebScraping().format_url(url)
        print(url)
        page_soup = WebScraping().create_page_soup(url)

        name = page_soup.findAll("div", {"class", "o9Xx3p _1_odLJ"})
        if not name:
            name = page_soup.findAll("div", {"class", "o9Xx3p A0eww2"})[0].text
            name_of_product = name.strip('Try This ')
            name_of_product = name_of_product[:-7]
        else:
            for row in name:
                name_of_product = row.text
                name_of_product = name_of_product[:-8]

        rating = page_soup.findAll("div", {"class", "_1i0wk8"})
        if not rating:
            rating_score = page_soup.findAll("div", {"class", "hGSR34 _2gBQ-6"})[0].text
        else:
            for row in rating:
                rating_score = row.text

        review = page_soup.findAll("div", {"class", "row _2yc1Qo"})
        if not review:
            review = page_soup.findAll("div", {"class", "_3HXBeF"})[0].text
            total_review = review.split(" ")[-2]
        else:
            for row in review:
                total_review = row.text

            total_review = total_review.rstrip(' Reviews')

        if ',' in total_review:
            list1 = total_review.split(',')
            string1 = ''.join(list1)
            total_review = int(string1)
        else:
            total_review = int(total_review)
        total_review = int(total_review)

        rating_score = float(rating_score)

        url_info = {'url': url, 'name_of_product': name_of_product, 'rating': rating_score,
                    'review': total_review}

        return url_info

    def format_url(self, url):
        parsed = urlparse.urlparse(url)
        pid = urlparse.parse_qs(parsed.query)['pid']
        sep = '?pid='
        url = url.split(sep, 1)[0]
        url = url.replace('/p/', '/product-reviews/')
        url = url + sep + pid[0]
        return url

    def create_page_soup(self, url):
        u_client = uReq(url)
        page_html = u_client.read()
        u_client.close()
        page_soup = soup(page_html, "html.parser")
        return page_soup


class Preprocessing:
    def clean_the_review(self, dirty_review):
        clean_review = demoji.replace(dirty_review, "")
        return clean_review


class SabKaMishran:
    product = {'Review_title': [], 'Review': [],
               'Rating': [], 'Score': []
               }

    features = {
        'cost': ['cost', 'money', 'price', 'cheap', 'expensive', 'costly', 'value', 'worth'],
        'quality': ['quality', 'durability', 'material', 'fitting', 'weight', 'balance', 'finish', 'damage'],
        'battery': ['battery', 'mah', 'charging', 'life', 'backup'],
        'display': ['display', 'screen', 'resolution'],
        'camera': ['camera', 'photo', 'selfie', 'mp', 'megapixel', 'flash'],
        'design': ['design', 'sleek', 'hefty', 'slim', 'lightweight', 'thick', 'look'],
        'performance': ['performance', 'slow', 'fast', 'speed', 'lag']
    }

    stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
                  "product", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its",
                  "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this",
                  "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has",
                  "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because",
                  "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into",
                  "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out",
                  "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where",
                  "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no",
                  "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just",
                  "don", "should", "now"]

    count = {
        'cost': [0, 0, 0],
        'quality': [0, 0, 0],
        'battery': [0, 0, 0],
        'display': [0, 0, 0],
        'camera': [0, 0, 0],
        'design': [0, 0, 0],
        'performance': [0, 0, 0]
    }

    vectorizer = pickle.load(
        open('D:/MyProjects/Final-Year-Project/scrapify/my_app/vectorizer_cellphone.sav', 'rb'))
    classifier = pickle.load(
        open('D:/MyProjects/Final-Year-Project/scrapify/my_app/classifier_cellphone.sav', 'rb'))

    # nlp = spacy.load("en_core_web_lg")
    tokenizer = nltk.RegexpTokenizer(r"\w+")

    def define_product(self):
        self.product = {'Review_title': [], 'Review': [],
                        'Rating': [], 'Score': []
                        }

    def define_count(self):
        self.count = {
            'cost': [0, 0, 0],
            'quality': [0, 0, 0],
            'battery': [0, 0, 0],
            'display': [0, 0, 0],
            'camera': [0, 0, 0],
            'design': [0, 0, 0],
            'performance': [0, 0, 0]
        }

    def get_aspects(self, x):
        doc = self.tokenizer.tokenize(x)
        # doc = self.nlp(x)  ## Tokenize and extract grammatical components
        doc = [i for i in doc if
               i not in self.stop_words]  ## Remove common words and retain only nouns
        # doc = list(map(lambda i: i.lower(), doc))  ## Normalize text to lower case
        # doc = pd.Series(doc)
        # doc = doc.index.tolist()
        return doc

    def find_feature_average(self, df, path_excel):

        aspects_list = []
        for i in range(len(df['Review'].to_list())):
            aspects = self.get_aspects(df['Review'][i])
            list1 = []
            for key in self.features.keys():
                if any(item in self.features[key] for item in aspects):
                    self.count[key][0] += 1
                    self.count[key][1] += df['Score'][i]
                    list1.append(key)
            aspects_list.append(list1)

        df['Aspects'] = aspects_list
        df.to_excel(path_excel, index=None, header=True)

        for key in self.count:
            if self.count[key][0] is not 0:
                avg = round(self.count[key][1] / self.count[key][0], 2)
                self.count[key][2] = avg - 0.2

    def count_value(self, path_excel):
        self.define_count()
        print(path_excel)
        df = pd.read_excel(path_excel)
        value = {}
        value['length'] = len(df['Review'].to_list())
        value['score'] = sum(df["Score"].to_list())
        average = round(value['score'] / value['length'], 2)
        value['average'] = average - 0.2
        value['path'] = path_excel
        self.find_feature_average(df, path_excel)
        value['count'] = self.count
        return value

    def analysis(self, url):
        page_html = requests.get(url).content

        page_soup = soup(page_html, "html.parser")

        containers = page_soup.findAll("div", {"class", "qwjRop _2675cp"})
        if not containers:
            containers = page_soup.findAll("div", {"class", "col _390CkK _1gY8H-"})

        for row in containers:

            self.product["Rating"].append(row.find_all("div", {"class", "hGSR34"})[0].text)
            review = row.findAll("div", {"class", "_2t8wE0"})

            if not review:
                self.product["Review_title"].append(row.find_all("p", {"class", "_2xg6Ul"})[0].text)
                review = row.findAll("div", {"class", "qwjRop"})[0].text
                review = review.rstrip('READ MORE')
                clean_review = Preprocessing().clean_the_review(review)
                self.product["Review"].append(clean_review)
                aspects = self.get_aspects(clean_review)
                vector = self.vectorizer.transform([clean_review])
                prediction_linear = self.classifier.predict(vector)
                self.product["Score"].append(prediction_linear[0])



            else:
                review = review[0].text
                review = review.rstrip('READ MORE')
                clean_review = Preprocessing().clean_the_review(review)
                self.product["Review"].append(clean_review)
                self.product["Review_title"].append(" ")
                aspects = self.get_aspects(clean_review)
                vector = self.vectorizer.transform([clean_review])
                prediction_linear = self.classifier.predict(vector)
                self.product["Score"].append(prediction_linear[0])

        return self.product


class Analyze:

    @shared_task(bind=True)
    def analyze_the_product(self, url, product_name):
        s = SabKaMishran()
        s.define_product()
        name_of_product = product_name
        page_soup = WebScraping().create_page_soup(url)
        containers = page_soup.findAll("div", {"class", "_2zg3yZ _3KSYCY"})

        page = containers[0].select('span')[0].text.split(" ")[-1]
        if ',' in page:
            list1 = page.split(',')
            string1 = ''.join(list1)
            pno = int(string1)
        else:
            pno = int(page)
        product_name = product_name[0:15] + str(datetime.datetime.now().microsecond)
        path1 = "static\\my_app\\product_reviews\\R_" + product_name + ".xlsx"
        if os.path.exists(path1):
            return 'Exists'
        else:
            progress_recorder = ProgressRecorder(self)
            for i in range(1, pno + 1):
                time.sleep(0.05)
                url1 = url + "&page=" + str(i)

                p = s.analysis(url1)

                progress_recorder.set_progress(i, pno, "Ye vaaala")

            df = DataFrame(s.product, columns=['Review_title', 'Review', 'Score', 'Rating'])

            df.to_excel(
                r'D:\MyProjects\Final-Year-Project\scrapify\my_app\static\my_app\product_reviews\R_' + product_name + '.xlsx',
                index=None, header=True)

            path_excel = 'D:/MyProjects/Final-Year-Project/scrapify/my_app/static/my_app/product_reviews/R_' + product_name + '.xlsx'

            l = Link.objects.filter(product_name=name_of_product)
            l.update(path=path_excel)

            return True

    def test_analysis(self):
        url = input("Enter product's URL")

        url_info = WebScraping().get_info_url(url)

        Analyze().analyze_the_product(url_info["url"], url_info["name_of_product"])
