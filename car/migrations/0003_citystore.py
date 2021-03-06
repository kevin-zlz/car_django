# Generated by Django 2.1.1 on 2018-10-13 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0002_auto_20181013_1610'),
    ]

    operations = [
        migrations.CreateModel(
            name='CityStore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('storename', models.CharField(max_length=50)),
                ('detailaddress', models.CharField(max_length=100)),
                ('storetel', models.CharField(max_length=30)),
                ('storetime', models.CharField(max_length=50)),
                ('storeaddress', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='car.City')),
            ],
        ),
    ]
