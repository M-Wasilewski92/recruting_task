from django.urls import path

from .views import PopulateDatabase, MakeLastUpdateRaport, UpdateDataBase

urlpatterns = [
    path('get_data/', PopulateDatabase.as_view()),
    path('update/', UpdateDataBase.as_view()),
    path('raport/', MakeLastUpdateRaport.as_view())
]
