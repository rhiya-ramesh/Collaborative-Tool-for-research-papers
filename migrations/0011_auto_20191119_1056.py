# Generated by Django 2.1.7 on 2019-11-19 05:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Collab_Docs', '0010_auto_20191119_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='comment_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 19, 10, 56, 6, 206275)),
        ),
    ]
