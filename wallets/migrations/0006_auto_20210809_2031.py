# Generated by Django 2.2.13 on 2021-08-09 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0005_auto_20210716_1458'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='beneficiary',
            unique_together={('user_id', 'account_number', 'ifsc')},
        ),
    ]
