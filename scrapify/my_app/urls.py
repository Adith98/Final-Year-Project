from django.urls import path
from . import views

app_name = 'my_app'
urlpatterns = [

    path('', views.IndexView.as_view(), name='index'),
    path('scrape/', views.ScrapeView.as_view(), name='name'),
    path('celery/', views.index, name='celery'),
]
