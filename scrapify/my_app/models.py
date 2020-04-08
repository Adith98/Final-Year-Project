from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Link(models.Model):
    url = models.URLField(max_length=10000)
    product_name = models.CharField(max_length=10000)
    review = models.IntegerField()
    rating = models.FloatField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name


