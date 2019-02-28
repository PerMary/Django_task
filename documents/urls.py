from django.urls import path
from . import views

app_name = "documents"

urlpatterns =[
    path('demand/<id_demand>/documents_list', views.documents_list, name='documents_list'),
]
