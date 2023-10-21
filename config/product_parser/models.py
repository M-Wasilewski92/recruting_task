from django.db import models
from django_unixdatetimefield import UnixDateTimeField


# Create your models here.
class XmlFile(models.Model):
    creation = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255)


class DateFields(models.Model):
    unixtime = UnixDateTimeField()
    datetime = models.DateTimeField()
    xml_file = models.ForeignKey(XmlFile, on_delete=models.CASCADE)


class Products(models.Model):
    xml_file = models.ForeignKey(XmlFile, on_delete=models.CASCADE)


class ProductField(models.Model):
    symbol = models.CharField(max_length=255, blank=True)
    ean = models.IntegerField(null=True)
    qty = models.IntegerField(null=True)
    model = models.CharField(max_length=255, blank=True)
    sizechart = models.URLField(blank=True)
    product_data = models.ForeignKey(Products, on_delete=models.CASCADE)


class ProductQtyUpdate(models.Model):
    created = models.DateTimeField(auto_now_add=True)


class ProductHistory(models.Model):
    old_qty = models.IntegerField(null=True)
    new_qty = models.IntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(ProductField, on_delete=models.CASCADE)
    qty_update = models.ForeignKey(ProductQtyUpdate, on_delete=models.CASCADE)
