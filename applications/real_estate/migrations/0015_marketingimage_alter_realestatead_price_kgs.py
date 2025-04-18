# Generated by Django 4.2.20 on 2025-04-11 12:32

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate', '0014_rename_real_estate_price_4105e8_idx_real_estate_price_813c41_idx_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarketingImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='Рекламное изображение')),
                ('property_type', models.CharField(choices=[('apartments', 'Квартиры'), ('houses', 'Дома'), ('commercials', 'Коммерческая недвижимость'), ('rooms', 'Комнаты'), ('plots', 'Участки'), ('dachas', 'Дачи'), ('parkings', 'Паркинги')], max_length=20, verbose_name='Тип недвижимости')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активно')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Рекламное изображение',
                'verbose_name_plural': 'Рекламные изображения',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AlterField(
            model_name='realestatead',
            name='price_kgs',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Цена в сомах'),
        ),
    ]
