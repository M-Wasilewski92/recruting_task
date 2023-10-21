from django.shortcuts import render, HttpResponse
from django.views import View
from .models import XmlFile, DateFields, ProductField, Products, ProductHistory, ProductQtyUpdate
import xml.etree.ElementTree as ET
import requests
from datetime import datetime

import time


# Create your views here.
class PopulateDatabase(View):

    def get(self, request):
        data_file = "qty.xml"
        xml_file = XmlFile(file_name=data_file)
        xml_file.save()
        URL = request.GET.get("xml_link")  # /get_data/?xml_link=

        response = requests.get(URL, verify=False)
        with open("qty.xml", "wb") as file:
            file.write(response.content)

        with open("qty.xml", "rb") as file:
            tree = ET.parse(file)
            root = tree.getroot()
            # date
            date_fields = DateFields()
            date_fields.unixtime = datetime.fromtimestamp(int(root[0][0].text))
            date_object = datetime.strptime(root[0][1].text, '%Y-%m-%d %H:%M:%S.%f')
            date_fields.datetime = date_object
            date_fields.xml_file = xml_file
            date_fields.save()
            # products
            products = Products()
            products.xml_file = xml_file
            products.save()
            models_to_save = []
            for child in root[1]:
                product_field = ProductField(symbol=child[0].text, ean=child[1].text, qty=child[2].text,
                                             model=child[3].text, sizechart=child[4].text, product_data=products)
                models_to_save.append(product_field)
            ProductField.objects.bulk_create(models_to_save)

        return render(request, template_name="populate.html")


class UpdateDataBase(View):
    def get(self, request):
        start = time.time()
        URL = request.GET.get("xml_link")  # /update/?xml_link=
        response = requests.get(URL, verify=False)
        with open("qty_update.xml", "wb") as file:
            file.write(response.content)
        update = ProductQtyUpdate()
        update.save()
        with open("qty_update.xml", "rb") as file:
            tree = ET.parse(file)
            root = tree.getroot()
            item_list = {}
            end = time.time()
            for child in root[1]:
                if child[2].text is not None:
                    new_ean = child[2].text
                    new_qty = int(child[3].text)
                item_list[f"{new_ean}"] = new_qty
            end = time.time()
            item_bulk_update_list = []
            for ean, new_qty in item_list.items():
                product = ProductField.objects.get(ean=ean)
                if product.qty != new_qty:
                    ProductHistory.objects.create(old_qty=product.qty, new_qty=new_qty, product=product,
                                                  qty_update=update)
                    product.qty = new_qty
                    item_bulk_update_list.append(product)
        ProductField.objects.bulk_update(item_bulk_update_list, ['qty'])
        return render(request, template_name="update.html", )


class MakeLastUpdateRaport(View):
    def get(self, request):
        update = ProductQtyUpdate.objects.latest("created")
        changes = ProductHistory.objects.filter(qty_update=update.id)
        to_http = ""
        with open("raport.txt", "w") as raport:
            for item in changes:
                raport.write(f" {item.product.ean}: {item.old_qty}----> {item.new_qty}| Time of Change: {item.created}\n")
                to_http += f" {item.product.ean}: {item.old_qty}----> {item.new_qty}| Time of Change: {item.created}<br>"
        return HttpResponse(to_http)
