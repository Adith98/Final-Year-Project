from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic

from .forms import GetLink
from .models import Link
from .webscraping import WebScraping as ws


# Create your views here.
class IndexView(generic.TemplateView):
    template_name = "my_app/index.html"

    def post(self, request):
        if request.method == 'POST':
            form = GetLink(request.POST)
            if form.is_valid():
                url = form.cleaned_data['link']
                url_info = get_info_url(url)
                args = {'form': form, 'url_info': url_info}
                return render(request, self.template_name, args)
            else:
                args = {'form': form}
                return render(request, self.template_name, args)

    def get(self, request):
        form = GetLink()
        args = {'form': form}
        return render(request, self.template_name, args)


class ScrapeView(generic.TemplateView):
    template_name = "my_app/name.html"

    def post(self, request):
        if request.method == 'POST':
            url = request.POST.get('link')
            product_name = request.POST['product']
            success = ws().extract_reviews_from_url(url, product_name)
            print(success)
            args = {'url': url, 'name_of_product': product_name}
            return render(request, self.template_name, args)


def save_link_to_database(request):
    if request.method == 'POST':
        url = request.POST.get('link')
        product_name = request.POST['product']
        review = request.POST['reviews']
        rating = request.POST['rating']
        # success = ws().extract_reviews_from_url(url, product_name)
        # print(success)
        entry = Link(url=url,
                     product_name=product_name,
                     review=review,
                     rating=rating)
        entry.save()
        args = {'url': url, 'name_of_product': product_name, 'rating': rating,
                'review': review, 'scrape': 'scrape'}
        return render(request, 'my_app/name.html', args)


def get_info_url(url):
    url = url
    url = ws().format_url(url)
    print(url)
    page_soup = ws().create_page_soup(url)

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
