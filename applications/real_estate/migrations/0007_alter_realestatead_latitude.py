# Generated by Django 4.2.20 on 2025-04-03 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate', '0006_alter_realestatead_latitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realestatead',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=15, max_digits=18, null=True, verbose_name='Широта'),
        ),
    ]
