# Generated by Django 4.2.20 on 2025-04-03 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate', '0004_alter_realestatead_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realestatead',
            name='latitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Широта'),
        ),
        migrations.AlterField(
            model_name='realestatead',
            name='longitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Долгота'),
        ),
    ]
