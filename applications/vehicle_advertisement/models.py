from django.core.cache import cache
from django.db import models
from django.db.models import CheckConstraint, Q
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from applications.vehicle.models import VehicleAd, VehicleBodyType, VehicleGeneration, Fuel, Drive, Transmission, \
    VehicleModification, VehicleCategory, Seria, CommercialType, SpecialType, MotoType, VehicleAdManager

User = get_user_model()


class SteeringChoices(models.TextChoices):
    left = ('left', _('Левый руль'))
    right = ('right', _('Правый руль'))


class PassengerCar(VehicleAd):
    title = models.CharField(
        verbose_name="название",
        blank=True,
        null=True,
        max_length=255
    )
    category = models.CharField(
        max_length=255,
        choices=VehicleCategory.choices,
        default='passenger',
        verbose_name='категория'
    )
    body_type = models.ForeignKey(
        VehicleBodyType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='passenger_car_vehicles',
        verbose_name=_('Тип кузова')
    )
    generation = models.ForeignKey(
        VehicleGeneration,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='passenger_car_generation',
        verbose_name=_('Поколение')
    )
    fuel_type = models.ForeignKey(
        Fuel,
        verbose_name=_('Двигатель'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='passenger_car_vehicle_fuel_type'
    )
    drive_type = models.ForeignKey(
        Drive,
        verbose_name=_('Привод'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='passenger_car_vehicle_drive_type'
    )
    transmission = models.ForeignKey(
        Transmission,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Коробка передач'),
        related_name='passenger_car_vehicle_transmission_type'
    )
    modification = models.ForeignKey(
        VehicleModification,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='passenger_car_modifications',
        verbose_name=_('Модификация')

    )
    steering = models.CharField(
        max_length=10,
        choices=SteeringChoices.choices,
        default='left',
        verbose_name=_('Расположение руля')
    )

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f"{self.make} {self.model} {self.price}{self.currency}"
        super().save(*args, **kwargs)

    objects = VehicleAdManager()

    class Meta:
        verbose_name = "Легковая машина"
        verbose_name_plural = "Легковые машины"


class CommercialCar(VehicleAd):
    title = models.CharField(
        verbose_name="название",
        blank=True,
        null=True,
        max_length=255
    )
    commercial_type = models.ForeignKey(
        CommercialType,
        verbose_name="тип",
        on_delete=models.SET_NULL,
        null=True,
        related_name="commercial_car_type"
    )
    category = models.CharField(
        max_length=255,
        choices=VehicleCategory.choices,
        default='commercial',
        verbose_name='категория'
    )
    body_type = models.ForeignKey(
        VehicleBodyType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='commercial_car_vehicles',
        verbose_name=_('Тип кузова')
    )
    generation = models.ForeignKey(
        VehicleGeneration,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='commercial_car_generation',
        verbose_name=_('Поколение')
    )
    fuel_type = models.ForeignKey(
        Fuel,
        verbose_name=_('Двигатель'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='commercial_car_vehicle_fuel_type'
    )
    drive_type = models.ForeignKey(
        Drive,
        verbose_name=_('Привод'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='commercial_car_vehicle_drive_type'
    )
    transmission = models.ForeignKey(
        Transmission,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Коробка передач'),
        related_name='commercial_car_vehicle_transmission_type'
    )
    modification = models.ForeignKey(
        VehicleModification,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='commercial_car_modifications',
        verbose_name=_('Модификация')

    )
    steering = models.CharField(
        max_length=10,
        choices=SteeringChoices.choices,
        default='left',
        verbose_name=_('Расположение руля')
    )

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f"{self.make} {self.model} {self.price}  {self.currency}"
        super().save(*args, **kwargs)

    objects = VehicleAdManager()

    class Meta:
        verbose_name = "Коммерческая машина"
        verbose_name_plural = "Коммерческие машины"


class SpecialCar(VehicleAd):
    title = models.CharField(
        verbose_name="название",
        blank=True,
        null=True,
        max_length=255
    )
    special_type = models.ForeignKey(
        SpecialType,
        verbose_name="тип",
        on_delete=models.SET_NULL,
        null=True,
        related_name="special_car_type"
    )
    category = models.CharField(
        max_length=255,
        choices=VehicleCategory.choices,
        default='special',
        verbose_name='категория'

    )
    fuel_type = models.ForeignKey(
        Fuel,
        verbose_name=_('Двигатель'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='special_car_vehicle_fuel_type'
    )
    steering = models.CharField(
        max_length=10,
        choices=SteeringChoices.choices,
        default='left',
        verbose_name=_('Расположение руля')
    )

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f"{self.make} {self.model} {self.price} {self.currency}"
        super().save(*args, **kwargs)

    objects = VehicleAdManager()

    class Meta:
        verbose_name = "Спецтехника"
        verbose_name_plural = "Спецтехника"


class Moto(VehicleAd):
    title = models.CharField(
        verbose_name="название",
        blank=True,
        null=True,
        max_length=255
    )
    moto_type = models.ForeignKey(
        MotoType,
        verbose_name="тип",
        on_delete=models.SET_NULL,
        null=True,
        related_name="moto_type"
    )
    category = models.CharField(
        max_length=255,
        choices=VehicleCategory.choices,
        default='moto'
    )
    seria = models.ForeignKey(
        Seria,
        verbose_name=_('Серия'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='moto_vehicle_seria'
    )
    modification = models.ForeignKey(
        VehicleModification,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='moto_modifications',
        verbose_name=_('Модификация')

    )

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f"{self.make} {self.model} {self.price} {self.currency}"
        super().save(*args, **kwargs)

    objects = VehicleAdManager()

    class Meta:
        verbose_name = "Мотоцикл"
        verbose_name_plural = "Мотоциклы"
