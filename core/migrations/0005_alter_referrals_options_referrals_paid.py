# Generated by Django 4.0.4 on 2022-07-25 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_referrals_referred_alter_referrals_referred_by'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='referrals',
            options={'verbose_name': 'referral'},
        ),
        migrations.AddField(
            model_name='referrals',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]
