# Generated by Django 2.2.13 on 2021-08-12 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_auto_20210812_1239'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playedgame',
            old_name='game',
            new_name='result',
        ),
        migrations.AddField(
            model_name='gameresult',
            name='published',
            field=models.IntegerField(default=0),
        ),
    ]
