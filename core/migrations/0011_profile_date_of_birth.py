# Generated by Django 4.0.4 on 2023-06-29 10:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_profile_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
