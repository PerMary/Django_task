from django.db import models
from django.conf import settings
from django.utils import timezone
from users.models import Profile
from myapp.models import Demand

# Create your models here.
class Documents(models.Model):
	date_create = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
	user_create = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Пользователь')
	id_demand = models.ForeignKey(Demand, on_delete=models.CASCADE, verbose_name='Заявка')
	name_doc = models.CharField(max_length=50, verbose_name='Название документа')
	url = models.CharField(max_length=250, verbose_name='Ссылка на файл')

	class Meta:
		permissions = (("can_view_create_documents", "Views create documents"),)
