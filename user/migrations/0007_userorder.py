# Generated by Django 2.1.1 on 2018-10-15 01:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0007_auto_20181015_0909'),
        ('user', '0006_auto_20181015_0928'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('takecartime', models.DateTimeField()),
                ('returncartime', models.DateTimeField()),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car.CarBase')),
                ('orderstate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.OrderState')),
                ('returncarplace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.ReturnCar')),
                ('takecarplace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car.CityStore')),
                ('yonghu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserBase')),
            ],
        ),
    ]
