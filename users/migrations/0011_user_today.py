# Generated by Django 2.2.13 on 2021-08-21 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20210820_2241'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='today',
            field=models.IntegerField(default=0),
        ),
    ]
