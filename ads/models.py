from django.db import models


class Ads(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    price = models.FloatField()
    description = models.CharField(max_length=1000)
    address = models.CharField(max_length=300)
    is_published = models.BooleanField()


class Categories(models.Model):
    name = models.CharField(max_length=100)
