#Определяет схемы URL для пользователей
from django.urls import path
from django.contrib.auth.views import login

from . import views

app_name = "users"

urlpatterns =[
    #Страница входа
    path('login/', login, {'template_name': 'users/login.html'}, name='login'),
    #Страница выхода
    path('logout/',views.logout_view, name='logout' ),
 ]
