# Generated by Django 2.1.1 on 2018-10-17 01:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('traval', '0004_auto_20181015_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userarisetravel',
            name='pubtime',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 17, 9, 46, 9, 433765)),
        ),
    ]
