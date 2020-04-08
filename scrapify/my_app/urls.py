from django.urls import path
from . import views

app_name = 'my_app'
urlpatterns = [

    path('', views.IndexView.as_view(), name='index'),
    path('save/', views.save_link_to_database, name='save-to-database'),
    path('scrape/', views.ScrapeView.as_view(), name='name'),

]
