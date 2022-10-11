from django.db import models


class Item(models.Model):

    itemname = models.CharField(max_length=50)
    photo = models.FileField()
    price = models.FloatField()
    quantity = models.IntegerField()
    date = models.DateField()
    days = models.CharField(max_length=3, null=True)
    description = models.CharField(max_length=1000)
    options = models.CharField(max_length=50)
