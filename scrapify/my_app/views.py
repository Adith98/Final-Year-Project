from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from celery.result import AsyncResult
import json

from .forms import GetLink
from .models import Link
from .webscraping import WebScraping as ws
from .pura_working import Analyze, SabKaMishran

from .backend import Progress


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
                if not Link.objects.filter(product_name=request.session['name_of_product']):
                    entry = Link(url=request.session['url'],
                                 product_name=request.session['name_of_product'],
                                 review=request.session['review'],
                                 rating=request.session['rating'])
                    entry.save()
                val = Link.objects.filter(product_name=request.session['name_of_product'])
                if str(val.values_list('path')[0][0]) != "":
                    value = SabKaMishran().count_value(str(val.values_list('path')[0][0]))
                    args = {'url': request.session['url'], 'name_of_product': request.session['name_of_product'],
                            'value': value,'rating':request.session['rating']}
                    return render(request, self.template_name, args)
                else:

                    path = Analyze().analyze_the_product.delay(request.session['url'],
                                                               request.session['name_of_product'])

                    args = {'url': request.session['url'], 'name_of_product': request.session['name_of_product'],
                            'task_id': path.task_id}
                    return render(request, self.template_name, args)
            else:
                return redirect('my_app:index')


def get_progress(request, task_id):
    progress = Progress(task_id)
    return HttpResponse(json.dumps(progress.get_info()), content_type='application/json')
