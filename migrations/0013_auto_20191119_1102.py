# Generated by Django 2.1.7 on 2019-11-19 05:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Collab_Docs', '0012_auto_20191119_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='comment_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 19, 11, 2, 14, 110384)),
        ),
    ]
