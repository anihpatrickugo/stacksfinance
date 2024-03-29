# Generated by Django 4.0.4 on 2023-06-28 10:39

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_plan_max_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='profile_photos'),
        ),
    ]
