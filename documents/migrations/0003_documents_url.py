# Generated by Django 2.0.10 on 2019-02-28 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_auto_20190228_1846'),
    ]

    operations = [
        migrations.AddField(
            model_name='documents',
            name='url',
            field=models.CharField(default=1, max_length=250, verbose_name='Ссылка на файл'),
            preserve_default=False,
        ),
    ]
