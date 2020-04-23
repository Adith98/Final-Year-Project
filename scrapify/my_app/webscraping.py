import datetime

import os
from pandas import DataFrame
import urllib.parse as urlparse
from urllib.request import urlopen as uReq
import requests
from bs4 import BeautifulSoup as soup
import time
from celery import shared_task

from .preprocessing import clean_the_review
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
            print(review)
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

    @shared_task(bind=True)
    def extract_reviews_from_url(self, url, product_name):

        name_of_product = product_name
        product_info = {'Review_title': [], 'Review': [],
                        'Rating': []
                        }
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
                # print(url1)
                # u_client = uReq(url1)
                page_html = requests.get(url1).content
                # u_client.close()
                page_soup = soup(page_html, "html.parser")

                containers = page_soup.findAll("div", {"class", "qwjRop _2675cp"})
                if not containers:
                    containers = page_soup.findAll("div", {"class", "col _390CkK _1gY8H-"})

                for row in containers:
                    rating = row.find_all("div", {"class", "hGSR34"})[0].text
                    review = row.findAll("div", {"class", "_2t8wE0"})

                    if not review:
                        review_title = row.find_all("p", {"class", "_2xg6Ul"})[0].text
                        review = row.findAll("div", {"class", "qwjRop"})[0].text
                        review = clean_the_review(review)

                        product_info["Review_title"].append(review_title)
                        product_info["Review"].append(review.rstrip('READ MORE'))
                        product_info["Rating"].append(rating)
                    else:
                        review = review[0].text
                        review = clean_the_review(review)

                        product_info["Review_title"].append(" ")
                        product_info["Review"].append(review.rstrip('READ MORE'))
                        product_info["Rating"].append(rating)

                progress_recorder.set_progress(i, pno, "Ye vaaala")

            df = DataFrame(product_info, columns=['Review_title', 'Review', 'Rating'])
            df.to_excel(
                r'C:\Users\shetty\Desktop\adith\Practice\Django\scrapify\my_app\static\my_app\product_reviews\R_' + product_name + '.xlsx',
                index=None, header=True)
            l = Link.objects.filter(product_name=name_of_product)
            l.update(path=path1)
            return True
