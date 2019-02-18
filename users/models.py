from django.db import models
from django.contrib.auth.models import User, UserManager

class Profile(User):
    middle_name = models.CharField(max_length=200, null=False, blank=True, default='', verbose_name='Отчество: ')
    objects = UserManager()

    class Meta:
        verbose_name= "Профиль"
        verbose_name_plural = "Профили"



