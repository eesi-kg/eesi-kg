# Generated by Django 4.2.20 on 2025-04-01 18:58

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='realestatead',
            name='house_number',
        ),
        migrations.RemoveField(
            model_name='realestatead',
            name='street_name',
        ),
        migrations.AddField(
            model_name='realestatead',
            name='address',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Адресс'),
        ),
        migrations.AddField(
            model_name='realestatead',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Широта'),
        ),
        migrations.AddField(
            model_name='realestatead',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Долгота'),
        ),
        migrations.AlterField(
            model_name='realestatead',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326, verbose_name='Долгота и Широта объекта'),
        ),
    ]
