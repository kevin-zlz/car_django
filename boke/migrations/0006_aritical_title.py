# Generated by Django 2.1.1 on 2018-10-24 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boke', '0005_articalcomment_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='aritical',
            name='title',
            field=models.CharField(default='这是文章标题', max_length=100),
        ),
    ]
