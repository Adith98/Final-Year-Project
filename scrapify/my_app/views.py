from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from celery.result import AsyncResult
import json

from .forms import GetLink
from .models import Link
from .webscraping import WebScraping as ws
from .tasks import sleepy, do_work


# Create your views here.
class IndexView(generic.TemplateView):
    template_name = "my_app/index.html"

    def post(self, request):
        if request.method == 'POST':
            form = GetLink(request.POST)
            if form.is_valid():
                url = form.cleaned_data['link']
                url_info = ws().get_info_url(url)
                request.session['url'] = url_info['url']
                request.session['name_of_product'] = url_info['name_of_product']
                request.session['review'] = url_info['review']
                request.session['rating'] = url_info['rating']
                args = {'form': form, 'url_info': url_info}
                return render(request, self.template_name, args)
            else:
                args = {'form': form}
                return render(request, self.template_name, args)

    def get(self, request):
        form = GetLink()
        args = {'form': form}
        request.session.flush()
        return render(request, self.template_name, args)


class ScrapeView(generic.TemplateView):
    template_name = "my_app/name.html"

    def get(self, request):
        if request.method == 'GET':
            if 'url' in request.session:
                if 'path' in request.session:
                    args = {'url': request.session['url'], 'name_of_product': request.session['name_of_product']}
                    return render(request, self.template_name, args)
                else:
                    path = ws().extract_reviews_from_url.delay(request.session['url'],
                                                               request.session['name_of_product'])

                    entry = Link(url=request.session['url'],
                                 product_name=request.session['name_of_product'],
                                 review=request.session['review'],
                                 rating=request.session['rating'])
                    entry.save()
                    args = {'url': request.session['url'], 'name_of_product': request.session['name_of_product'],
                            'task_id': path.task_id}
                    return render(request, self.template_name, args)
            else:
                return redirect('my_app:index')


def index(request):
    result = do_work.delay()
    return render(request, 'my_app/progress.html', context={'task_id': result.task_id})
