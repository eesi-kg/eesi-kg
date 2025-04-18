# Generated by Django 4.2.20 on 2025-04-01 18:16

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=255, unique=True, verbose_name='Город')),
                ('ordering', models.PositiveIntegerField(blank=True, null=True, verbose_name='Очередность')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
                'ordering': ['ordering', 'region'],
            },
        ),
        migrations.CreateModel(
            name='CountryName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Страна')),
                ('flag', models.ImageField(blank=True, null=True, upload_to='country_flags/', verbose_name='Флаг')),
            ],
            options={
                'verbose_name': 'Страна',
                'verbose_name_plural': 'Страны',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(choices=[('KGS', 'сом'), ('USD', 'дол. США')], max_length=255, verbose_name='валюта')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='currency_logos/', verbose_name='эмблема')),
            ],
            options={
                'verbose_name': 'Валюта',
                'verbose_name_plural': 'Валюты',
            },
        ),
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exchange_type', models.CharField(max_length=255, verbose_name='тип обмена')),
            ],
            options={
                'verbose_name': 'Тип обмена',
                'verbose_name_plural': 'Типы обмена',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=255, unique=True, verbose_name='Область')),
                ('ordering', models.PositiveIntegerField(blank=True, null=True, verbose_name='Очередность')),
            ],
            options={
                'verbose_name': 'Регион',
                'verbose_name_plural': 'Регионы',
                'ordering': ['ordering', 'region'],
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration_days', models.PositiveIntegerField(default=30, verbose_name='Длительность объявления')),
                ('days_before_notification', models.PositiveSmallIntegerField(default=3, verbose_name='Количество дней перед уведомлением')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Цена в день')),
                ('discount', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Скидка в %')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district', models.CharField(max_length=255, unique=True, verbose_name='Район')),
                ('ordering', models.PositiveIntegerField(blank=True, null=True, verbose_name='Очередность')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='district_city', to='common.city', verbose_name='Район')),
            ],
            options={
                'verbose_name': 'Район',
                'verbose_name_plural': 'Район',
                'ordering': ['ordering', 'district'],
            },
        ),
        migrations.AddField(
            model_name='city',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='city_region', to='common.region', verbose_name='Регион'),
        ),
    ]
