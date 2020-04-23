from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'my_app'
urlpatterns = [

    path('', views.IndexView.as_view(), name='index'),
    path('scrape/', views.ScrapeView.as_view(), name='name'),
    url(r'^(?P<task_id>[\w-]+)/$', views.get_progress, name='task_status'),
]
