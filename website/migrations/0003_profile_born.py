# Generated by Django 3.1.4 on 2021-01-22 10:10

from django.db import migrations, models
from datetime import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20210119_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='born',
            field=models.DateField(default=datetime.now().date()),
            preserve_default=False,
        ),
    ]
