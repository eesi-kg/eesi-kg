# Generated by Django 4.2.20 on 2025-04-03 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate', '0005_alter_realestatead_latitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realestatead',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=14, max_digits=17, null=True, verbose_name='Широта'),
        ),
        migrations.AlterField(
            model_name='realestatead',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=14, max_digits=17, null=True, verbose_name='Долгота'),
        ),
    ]
