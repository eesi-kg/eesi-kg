# Generated by Django 4.2.20 on 2025-04-06 18:50

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate', '0007_alter_realestatead_latitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realestateadimage',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='Фотография'),
        ),
    ]
