# Generated by Django 2.1.1 on 2018-10-18 05:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_userbase_icon'),
    ]

    operations = [
        migrations.RenameField(
            model_name='returncar',
            old_name='returncarplace',
            new_name='returncar',
        ),
    ]
