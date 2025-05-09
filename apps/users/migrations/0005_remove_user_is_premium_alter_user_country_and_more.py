# Generated by Django 4.2.20 on 2025-05-05 15:27

import apps.core.services
from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_color_user_groups_user_is_premium_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_premium',
        ),
        migrations.AlterField(
            model_name='user',
            name='country',
            field=django_countries.fields.CountryField(default='VN', max_length=2, verbose_name='country'),
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='', upload_to=apps.core.services.get_path_upload_image_user, verbose_name='image'),
        ),
    ]
