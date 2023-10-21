from django.contrib import admin
from .models import XmlFile, DateFields, Products, ProductField, ProductHistory, ProductQtyUpdate


# Register your models here.
admin.site.register(XmlFile)
admin.site.register(DateFields)
admin.site.register(Products)
admin.site.register(ProductField)
admin.site.register(ProductHistory)
admin.site.register(ProductQtyUpdate)

