# Generated by Django 2.2.2 on 2021-07-21 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('level', '0011_auto_20210721_1633'),
    ]

    operations = [
        migrations.RenameField(
            model_name='levelincomesettings',
            old_name='direct_commission_percentage',
            new_name='return_amount',
        ),
    ]
