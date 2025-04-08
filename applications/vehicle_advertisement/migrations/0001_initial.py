# Generated by Django 4.2.20 on 2025-04-01 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vehicle', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecialCar',
            fields=[
                ('vehiclead_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='vehicle.vehiclead')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='название')),
                ('category', models.CharField(choices=[('passenger', 'легковые'), ('commercial', 'коммерческие'), ('special', 'спец.техника'), ('moto', 'мотоциклы')], default='special', max_length=255, verbose_name='категория')),
                ('steering', models.CharField(choices=[('left', 'Левый руль'), ('right', 'Правый руль')], default='left', max_length=10, verbose_name='Расположение руля')),
                ('fuel_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='special_car_vehicle_fuel_type', to='vehicle.fuel', verbose_name='Двигатель')),
                ('special_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='special_car_type', to='vehicle.specialtype', verbose_name='тип')),
            ],
            options={
                'verbose_name': 'Спецтехника',
                'verbose_name_plural': 'Спецтехника',
            },
            bases=('vehicle.vehiclead',),
        ),
        migrations.CreateModel(
            name='PassengerCar',
            fields=[
                ('vehiclead_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='vehicle.vehiclead')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='название')),
                ('category', models.CharField(choices=[('passenger', 'легковые'), ('commercial', 'коммерческие'), ('special', 'спец.техника'), ('moto', 'мотоциклы')], default='passenger', max_length=255, verbose_name='категория')),
                ('steering', models.CharField(choices=[('left', 'Левый руль'), ('right', 'Правый руль')], default='left', max_length=10, verbose_name='Расположение руля')),
                ('body_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='passenger_car_vehicles', to='vehicle.vehiclebodytype', verbose_name='Тип кузова')),
                ('drive_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='passenger_car_vehicle_drive_type', to='vehicle.drive', verbose_name='Привод')),
                ('fuel_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='passenger_car_vehicle_fuel_type', to='vehicle.fuel', verbose_name='Двигатель')),
                ('generation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='passenger_car_generation', to='vehicle.vehiclegeneration', verbose_name='Поколение')),
                ('modification', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='passenger_car_modifications', to='vehicle.vehiclemodification', verbose_name='Модификация')),
                ('transmission', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='passenger_car_vehicle_transmission_type', to='vehicle.transmission', verbose_name='Коробка передач')),
            ],
            options={
                'verbose_name': 'Легковая машина',
                'verbose_name_plural': 'Легковые машины',
            },
            bases=('vehicle.vehiclead',),
        ),
        migrations.CreateModel(
            name='Moto',
            fields=[
                ('vehiclead_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='vehicle.vehiclead')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='название')),
                ('category', models.CharField(choices=[('passenger', 'легковые'), ('commercial', 'коммерческие'), ('special', 'спец.техника'), ('moto', 'мотоциклы')], default='moto', max_length=255)),
                ('modification', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='moto_modifications', to='vehicle.vehiclemodification', verbose_name='Модификация')),
                ('moto_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='moto_type', to='vehicle.mototype', verbose_name='тип')),
                ('seria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='moto_vehicle_seria', to='vehicle.seria', verbose_name='Серия')),
            ],
            options={
                'verbose_name': 'Мотоцикл',
                'verbose_name_plural': 'Мотоциклы',
            },
            bases=('vehicle.vehiclead',),
        ),
        migrations.CreateModel(
            name='CommercialCar',
            fields=[
                ('vehiclead_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='vehicle.vehiclead')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='название')),
                ('category', models.CharField(choices=[('passenger', 'легковые'), ('commercial', 'коммерческие'), ('special', 'спец.техника'), ('moto', 'мотоциклы')], default='commercial', max_length=255, verbose_name='категория')),
                ('steering', models.CharField(choices=[('left', 'Левый руль'), ('right', 'Правый руль')], default='left', max_length=10, verbose_name='Расположение руля')),
                ('body_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='commercial_car_vehicles', to='vehicle.vehiclebodytype', verbose_name='Тип кузова')),
                ('commercial_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='commercial_car_type', to='vehicle.commercialtype', verbose_name='тип')),
                ('drive_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='commercial_car_vehicle_drive_type', to='vehicle.drive', verbose_name='Привод')),
                ('fuel_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='commercial_car_vehicle_fuel_type', to='vehicle.fuel', verbose_name='Двигатель')),
                ('generation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='commercial_car_generation', to='vehicle.vehiclegeneration', verbose_name='Поколение')),
                ('modification', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='commercial_car_modifications', to='vehicle.vehiclemodification', verbose_name='Модификация')),
                ('transmission', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='commercial_car_vehicle_transmission_type', to='vehicle.transmission', verbose_name='Коробка передач')),
            ],
            options={
                'verbose_name': 'Коммерческая машина',
                'verbose_name_plural': 'Коммерческие машины',
            },
            bases=('vehicle.vehiclead',),
        ),
    ]
