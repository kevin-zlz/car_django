# Generated by Django 2.1.1 on 2018-10-17 01:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('traval', '0005_auto_20181017_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userarisetravel',
            name='pubtime',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 17, 9, 56, 50, 500715)),
        ),
    ]
