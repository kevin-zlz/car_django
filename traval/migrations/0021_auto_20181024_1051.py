# Generated by Django 2.1.1 on 2018-10-24 02:51

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('traval', '0020_auto_20181024_1047'),
    ]

    operations = [
        migrations.AddField(
            model_name='userarisetravel',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='traval.CityIcon'),
        ),
        migrations.AlterField(
            model_name='userarisetravel',
            name='pubtime',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 24, 10, 51, 33, 531844)),
        ),
    ]
