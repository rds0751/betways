# Generated by Django 2.2.13 on 2021-08-21 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0006_dragon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dragon',
            name='starting_amount',
            field=models.DecimalField(decimal_places=2, default=3.3, max_digits=3),
        ),
    ]