from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Documents(models.Model):
	date_create = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
	user_create = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
	name_doc = models.CharField(max_length=50, verbose_name='Название документа')
