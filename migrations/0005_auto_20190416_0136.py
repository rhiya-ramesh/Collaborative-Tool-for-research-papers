# Generated by Django 2.1.5 on 2019-04-15 20:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Collab_Docs', '0004_auto_20190412_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='documents',
            name='approve',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='comments',
            name='comment_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 16, 1, 36, 53, 151421)),
        ),
    ]
