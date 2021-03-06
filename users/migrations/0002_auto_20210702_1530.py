# Generated by Django 2.2.2 on 2021-07-02 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Top',
        ),
        migrations.RemoveField(
            model_name='user',
            name='all_wallets',
        ),
        migrations.RemoveField(
            model_name='user',
            name='app_directs',
        ),
        migrations.RemoveField(
            model_name='user',
            name='app_temp',
        ),
        migrations.RemoveField(
            model_name='user',
            name='app_wallet',
        ),
        migrations.RemoveField(
            model_name='user',
            name='auto_neft',
        ),
        migrations.RemoveField(
            model_name='user',
            name='binary_directs',
        ),
        migrations.RemoveField(
            model_name='user',
            name='binary_income',
        ),
        migrations.RemoveField(
            model_name='user',
            name='binary_rewards_level',
        ),
        migrations.RemoveField(
            model_name='user',
            name='cash_back',
        ),
        migrations.RemoveField(
            model_name='user',
            name='friends',
        ),
        migrations.RemoveField(
            model_name='user',
            name='imps_daily',
        ),
        migrations.RemoveField(
            model_name='user',
            name='income',
        ),
        migrations.RemoveField(
            model_name='user',
            name='left_pending',
        ),
        migrations.RemoveField(
            model_name='user',
            name='left_side_business',
        ),
        migrations.RemoveField(
            model_name='user',
            name='login_bonus',
        ),
        migrations.RemoveField(
            model_name='user',
            name='new_funds',
        ),
        migrations.RemoveField(
            model_name='user',
            name='recharge_limit',
        ),
        migrations.RemoveField(
            model_name='user',
            name='recharge_limit_used',
        ),
        migrations.RemoveField(
            model_name='user',
            name='redeem_access',
        ),
        migrations.RemoveField(
            model_name='user',
            name='referal',
        ),
        migrations.RemoveField(
            model_name='user',
            name='right_pending',
        ),
        migrations.RemoveField(
            model_name='user',
            name='right_side_business',
        ),
        migrations.RemoveField(
            model_name='user',
            name='royalty',
        ),
        migrations.RemoveField(
            model_name='user',
            name='secondary_cashback',
        ),
        migrations.RemoveField(
            model_name='user',
            name='service_access',
        ),
        migrations.RemoveField(
            model_name='user',
            name='shopping_wallet',
        ),
        migrations.RemoveField(
            model_name='user',
            name='tasks_done',
        ),
        migrations.RemoveField(
            model_name='user',
            name='today_binary_income',
        ),
        migrations.RemoveField(
            model_name='user',
            name='total_app_income',
        ),
        migrations.RemoveField(
            model_name='user',
            name='total_income',
        ),
        migrations.RemoveField(
            model_name='user',
            name='total_users_left',
        ),
        migrations.RemoveField(
            model_name='user',
            name='total_users_right',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_type',
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
    ]
