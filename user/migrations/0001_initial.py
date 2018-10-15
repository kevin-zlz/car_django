# Generated by Django 2.1.1 on 2018-10-13 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.CharField(max_length=30, unique=True)),
                ('telephone', models.CharField(max_length=30, unique=True)),
                ('password', models.CharField(max_length=30)),
                ('pub_time', models.DateTimeField(auto_now_add=True)),
                ('email', models.CharField(max_length=50, null=True)),
            ],
        ),
    ]
