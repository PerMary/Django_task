from django.urls import path
from . import views

app_name = "documents"

urlpatterns =[
    path('documents_list/', views.documents_list, name='documents_list'),
    path('create_pdf/', views.create_pdf, name='create_pdf'),
]