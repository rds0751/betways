# Generated by Django 2.2.13 on 2021-08-21 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0008_dragon_odds'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dragon',
            name='odds',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
