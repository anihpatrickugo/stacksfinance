# Generated by Django 4.0.4 on 2022-08-12 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_plan_max_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='max_amount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
