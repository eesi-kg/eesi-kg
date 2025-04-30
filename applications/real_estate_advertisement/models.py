from django.db import models
from django.utils.translation import gettext_lazy as _

from applications.real_estate.models import RealEstateAd, RoomType, ResidentialComplex, Series, BuildingType, Year, \
    Floor, ObjectType, RoomLocation
from core import settings
from django.contrib.auth.models import User


class PropertyTypeChoices(models.TextChoices):
    apartments = ('apartments', _('квартира'))
    houses = ('houses', _('дом'))
    commercials = ('commercials', _('коммерция'))
    rooms = ('rooms', _('комната'))
    plots = ('plots', _('участок'))
    dachas = ('dachas', _('дача'))
    parking_garages = ('parkings', _('паркинг/гараж'))


class ApartmentAd(RealEstateAd):
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='заголовок')
    property_type = models.CharField(
        verbose_name="тип недвижимости", max_length=255, choices=PropertyTypeChoices.choices, default="apartments"
    )
    rooms = models.ForeignKey(
        RoomType,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Количество комнат",
        related_name='apartment_ad_rooms'
    )
    residential_complex = models.ForeignKey(
        ResidentialComplex,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Жилой комплекс",
        related_name='apartment_ad_residential_complex'
    )
    series = models.ForeignKey(
        Series,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Серия дома",
        related_name='apartment_ad_series'
    )
    building_type = models.ForeignKey(
        BuildingType,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Тип строения",
        related_name='apartment_ad_building_type'
    )
    construction_year = models.ForeignKey(
        Year,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="construction_year",
        verbose_name="год постройки"
    )
    floor = models.ForeignKey(
        Floor,
        on_delete=models.SET_NULL,
        null=True,
        related_name="apartment_floor",
        verbose_name="этаж"
    )
    max_floor = models.ForeignKey(
        Floor,
        on_delete=models.SET_NULL,
        null=True,
        related_name="apartment_max_floor",
        verbose_name="количество этажей"
    )
    total_area = models.PositiveSmallIntegerField(
        verbose_name="общая площадь"
    )
    living_area = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name="жилая площадь"
    )
    kitchen_area = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name="площадь кухни"
    )

    def __str__(self):
        return f"{self.get_ad_type_display()} {self.rooms} {self.property_type} "

    def clean(self):
        from django.core.exceptions import ValidationError
        try:
            if int(self.floor.floor) > int(self.max_floor.floor):
                raise ValidationError("Количество этажей не может превышать общее количество этажей.")
        except:
            raise ValidationError("Нет этажей.")

    def save(self, *args, **kwargs):
        if self.ad_type == 'sale':
            self.title = f"Продается {self.get_property_type_display()}"
        elif self.ad_type == 'rent':
            self.title = f"Сдается {self.get_property_type_display()}"
        super().save(*args, **kwargs)

    def get_qr_url(self):
        base_url = getattr(settings, 'QR_BASE_URL')
        return f"{base_url}/real-estate/{self.property_type}/{self.public_id}/"

    class Meta:
        verbose_name = "Квартира"
        verbose_name_plural = "Квартиры"
        

class HouseAd(RealEstateAd):
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='заголовок')
    property_type = models.CharField(
        verbose_name="тип недвижимости", max_length=255, choices=PropertyTypeChoices.choices, default="houses"
    )
    rooms = models.ForeignKey(
        RoomType,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Количество комнат",
        related_name='house_ad_rooms'
    )
    building_type = models.ForeignKey(
        BuildingType,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Тип строения",
        related_name='house_ad_building_type'
    )
    floor = models.ForeignKey(
        Floor,
        on_delete=models.SET_NULL,
        null=True,
        related_name="house_floor",
        verbose_name="этаж"
    )
    area = models.PositiveSmallIntegerField(
        verbose_name="площадь дома m2"
    )
    total_area = models.PositiveSmallIntegerField(
        verbose_name="площадь участка, соток", blank=True, null=True
    )

    def __str__(self):
        return f"{self.get_ad_type_display()} {self.title}"

    def save(self, *args, **kwargs):
        if self.ad_type == 'sale':
            self.title = f"Продается {self.get_property_type_display()}"
        elif self.ad_type == 'rent':
            self.title = f"Сдается {self.get_property_type_display()}"
        super().save(*args, **kwargs)

    def get_qr_url(self):
        base_url = getattr(settings, 'QR_BASE_URL')
        return f"{base_url}/real-estate/{self.property_type}/{self.public_id}/"

    class Meta:
        verbose_name = "Дом"
        verbose_name_plural = "Дома"


class CommercialAd(RealEstateAd):
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='заголовок')
    property_type = models.CharField(
        verbose_name="тип недвижимости", max_length=255, choices=PropertyTypeChoices.choices, default="commercials"
    )
    object_type = models.ForeignKey(
        ObjectType,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Тип объекта",
        related_name='commercial_ad_object_type'
    )
    residential_complex = models.ForeignKey(
        ResidentialComplex,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Жилой комплекс",
        related_name='commercial_ad_residential_complex'
    )
    building_type = models.ForeignKey(
        BuildingType,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Тип строения",
        related_name='commercial_ad_building_type'
    )
    construction_year = models.ForeignKey(
        Year,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="commercial_year",
        verbose_name="год постройки"
    )
    floor = models.ForeignKey(
        Floor,
        on_delete=models.SET_NULL,
        null=True,
        related_name="commercial_floor",
        verbose_name="этаж"
    )
    max_floor = models.ForeignKey(
        Floor,
        on_delete=models.SET_NULL,
        null=True,
        related_name="commercial_max_floor",
        verbose_name="количество этажей"
    )
    total_area = models.PositiveSmallIntegerField(
        verbose_name="площадь коммерческой недвижимости m2"
    )

    def __str__(self):
        return f"{self.get_ad_type_display()}, {self.title}"

    def clean(self):
        from django.core.exceptions import ValidationError
        try:
            if int(self.floor.floor) > int(self.max_floor.floor):
                raise ValidationError("Количество этажей не может превышать общее количество этажей.")
        except:
            raise ValidationError("Нет этажей.")

    def save(self, *args, **kwargs):
        if self.ad_type == 'sale':
            self.title = f"Продается {self.get_property_type_display()}"
        elif self.ad_type == 'rent':
            self.title = f"Сдается {self.get_property_type_display()}"
        super().save(*args, **kwargs)

    def get_qr_url(self):
        base_url = getattr(settings, 'QR_BASE_URL')
        return f"{base_url}/real-estate/{self.property_type}/{self.public_id}/"

    class Meta:
        verbose_name = "Коммерческое помещение"
        verbose_name_plural = "Коммерческие помещения"


class RoomAd(RealEstateAd):
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='заголовок')
    property_type = models.CharField(
        verbose_name="тип недвижимости", max_length=255, choices=PropertyTypeChoices.choices, default="rooms"
    )
    rooms = models.ForeignKey(
        RoomType,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Количество комнат",
        related_name='room_ad_rooms'
    )
    room_location = models.ForeignKey(
        RoomLocation,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Расположение",
        related_name='room_ad_location'
    )
    floor = models.ForeignKey(
        Floor,
        on_delete=models.SET_NULL,
        null=True,
        related_name="room_ad_floor",
        verbose_name="этаж"
    )
    max_floor = models.ForeignKey(
        Floor,
        on_delete=models.SET_NULL,
        null=True,
        related_name="room_ad_max_floor",
        verbose_name="количество этажей"
    )
    total_area = models.PositiveSmallIntegerField(
        verbose_name="площадь участка"
    )
    living_area = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name="жилая площадь"
    )
    kitchen_area = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name="площадь кухни"
    )

    def __str__(self):
        return f"{self.get_ad_type_display()} {self.title}"

    def clean(self):
        from django.core.exceptions import ValidationError
        try:
            if int(self.floor.floor) > int(self.max_floor.floor):
                raise ValidationError("Количество этажей не может превышать общее количество этажей.")
        except:
            raise ValidationError("Нет этажей.")

    def save(self, *args, **kwargs):
        if self.ad_type == 'sale':
            self.title = f"Продается {self.get_property_type_display()}"
        elif self.ad_type == 'rent':
            self.title = f"Сдается {self.get_property_type_display()}"
        super().save(*args, **kwargs)

    def get_qr_url(self):
        base_url = getattr(settings, 'QR_BASE_URL')
        return f"{base_url}/real-estate/{self.property_type}/{self.public_id}/"

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"


class PlotAd(RealEstateAd):
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='заголовок')
    property_type = models.CharField(
        verbose_name="тип недвижимости", max_length=255, choices=PropertyTypeChoices.choices, default="plots"
    )
    total_area = models.PositiveSmallIntegerField(
        verbose_name="площадь участка, соток"
    )

    def __str__(self):
        return f"{self.get_ad_type_display()} {self.title}"

    def save(self, *args, **kwargs):
        if self.ad_type == 'sale':
            self.title = f"Продается {self.get_property_type_display()}"
        elif self.ad_type == 'rent':
            self.title = f"Сдается {self.get_property_type_display()}"
        super().save(*args, **kwargs)

    def get_qr_url(self):
        base_url = getattr(settings, 'QR_BASE_URL')
        return f"{base_url}/real-estate/{self.property_type}/{self.public_id}/"

    class Meta:
        verbose_name = "Участок"
        verbose_name_plural = "Участки"


class DachaAd(RealEstateAd):
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='заголовок')
    property_type = models.CharField(
        verbose_name="тип недвижимости", max_length=255, choices=PropertyTypeChoices.choices, default="dachas"
    )
    rooms = models.ForeignKey(
        RoomType,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Количество комнат",
        related_name='dacha_ad_rooms'
    )
    building_type = models.ForeignKey(
        BuildingType,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Тип строения",
        related_name='dacha_ad_building_type'
    )
    area = models.PositiveSmallIntegerField(
        verbose_name="площадь дачи m2"
    )
    total_area = models.PositiveSmallIntegerField(
        verbose_name="общая площадь, соток"
    )

    def __str__(self):
        return f"{self.get_ad_type_display()} {self.title}"

    def save(self, *args, **kwargs):
        if self.ad_type == 'sale':
            self.title = f"Продается {self.get_property_type_display()}"
        elif self.ad_type == 'rent':
            self.title = f"Сдается {self.get_property_type_display()}"
        super().save(*args, **kwargs)

    def get_qr_url(self):
        base_url = getattr(settings, 'QR_BASE_URL')
        return f"{base_url}/real-estate/{self.property_type}/{self.public_id}/"

    class Meta:
        verbose_name = "Дача"
        verbose_name_plural = "Дачи"


class ParkingAd(RealEstateAd):
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='заголовок')
    property_type = models.CharField(
        verbose_name="тип недвижимости", max_length=255, choices=PropertyTypeChoices.choices, default="parkings"
    )
    residential_complex = models.ForeignKey(
        ResidentialComplex,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Жилой комплекс",
        related_name='parking_ad_residential_complex'
    )

    def __str__(self):
        return f"{self.get_ad_type_display()} {self.residential_complex}"

    def save(self, *args, **kwargs):
        if self.ad_type == 'sale':
            self.title = f"Продается {self.get_property_type_display()}"
        elif self.ad_type == 'rent':
            self.title = f"Сдается {self.get_property_type_display()}"
        super().save(*args, **kwargs)

    def get_qr_url(self):
        base_url = getattr(settings, 'QR_BASE_URL')
        return f"{base_url}/real-estate/{self.property_type}/{self.public_id}/"

    class Meta:
        verbose_name = "Паркинг"
        verbose_name_plural = "Паркинг"


class FCMToken(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='fcm_tokens',
        verbose_name='User'
    )
    token = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='FCM Token'
    )
    device_type = models.CharField(
        max_length=50,
        choices=[
            ('ios', 'iOS'),
            ('android', 'Android')
        ],
        verbose_name='Device Type'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated At'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Is Active'
    )

    class Meta:
        verbose_name = 'FCM Token'
        verbose_name_plural = 'FCM Tokens'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.device_type}"
