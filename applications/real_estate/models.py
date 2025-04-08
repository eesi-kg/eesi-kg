from datetime import timedelta

import qrcode
import cloudinary.uploader
from io import BytesIO

from cloudinary_storage.storage import RawMediaCloudinaryStorage
from django.contrib.gis.db.models import PointField

from django.core.validators import RegexValidator

from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from applications.common.models import Currency, Exchange, Region, City, District, \
    generate_short_id, Subscription
from django.contrib.auth import get_user_model

from django.db import models
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField

from applications.user.tasks import logger

User = get_user_model()


class Telephone(models.Model):
    telephone = models.CharField(max_length=255, unique=True, verbose_name='телефон')

    def __str__(self):
        return self.telephone

    class Meta:
        verbose_name = 'Телефон'
        verbose_name_plural = 'Телефоны'


class Internet(models.Model):
    internet = models.CharField(max_length=255, unique=True, verbose_name='интернет')

    def __str__(self):
        return self.internet

    class Meta:
        verbose_name = 'Интернет'
        verbose_name_plural = 'Интернеты'


class BathRoom(models.Model):
    bathroom = models.CharField(max_length=255, unique=True, verbose_name='санузел')

    def __str__(self):
        return self.bathroom

    class Meta:
        verbose_name = 'Санузел'
        verbose_name_plural = 'Санузлы'


class Gas(models.Model):
    gas = models.CharField(max_length=255, unique=True, verbose_name='газ')

    def __str__(self):
        return self.gas

    class Meta:
        verbose_name = 'Газ'
        verbose_name_plural = 'Газ'


class Balcony(models.Model):
    balcony = models.CharField(max_length=255, unique=True, verbose_name='балкон')

    def __str__(self):
        return self.balcony

    class Meta:
        verbose_name = 'Балкон'
        verbose_name_plural = 'Балконы'


class MainDoor(models.Model):
    main_door = models.CharField(max_length=255, unique=True, verbose_name='входная дверь')

    def __str__(self):
        return self.main_door

    class Meta:
        verbose_name = 'Входная дверь'
        verbose_name_plural = 'Входные двери'


class Parking(models.Model):
    parking = models.CharField(max_length=255, unique=True, verbose_name='парковка')

    def __str__(self):
        return self.parking

    class Meta:
        verbose_name = 'Парковка'
        verbose_name_plural = 'Парковки'


class Furniture(models.Model):
    furniture = models.CharField(max_length=255, unique=True, verbose_name='мебель')

    def __str__(self):
        return self.furniture

    class Meta:
        verbose_name = 'Мебель'
        verbose_name_plural = 'Мебели'


class FloorType(models.Model):
    floor_type = models.CharField(max_length=255, unique=True, verbose_name='пол')

    def __str__(self):
        return self.floor_type

    class Meta:
        verbose_name = 'Пол'
        verbose_name_plural = 'Пол'


class Safety(models.Model):
    safety = models.CharField(max_length=255, unique=True, verbose_name='безапасность')

    def __str__(self):
        return self.safety

    class Meta:
        verbose_name = 'Безапасность'
        verbose_name_plural = 'Безапасности'


class Other(models.Model):
    other = models.CharField(max_length=255, unique=True, verbose_name='Разное')

    def __str__(self):
        return self.other

    class Meta:
        verbose_name = 'разное'
        verbose_name_plural = 'разные'


class Document(models.Model):
    document = models.CharField(max_length=255, unique=True, verbose_name='Документы')

    def __str__(self):
        return self.document

    class Meta:
        verbose_name = 'документ'
        verbose_name_plural = 'документы'


class Developer(models.Model):
    name = models.CharField("Застройщик", max_length=255, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Застройщик"
        verbose_name_plural = "Застройщики"


class ResidentialComplex(models.Model):
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, related_name='developer',
                                  verbose_name='Застройщик')
    name = models.CharField("Название ЖК", max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жилой Комплекс"
        verbose_name_plural = "Жилые Комплексы"


class Series(models.Model):
    name = models.CharField("Серия дома", max_length=255, unique=True)
    description = models.TextField("Описание", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Серия"
        verbose_name_plural = "Серии"


class BuildingType(models.Model):
    name = models.CharField("Тип строения", max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Строение"
        verbose_name_plural = "Строения"


class HeatingType(models.Model):
    name = models.CharField("Тип отопления", max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Отопление"
        verbose_name_plural = "Отопления"


class ConditionType(models.Model):
    name = models.CharField("Состояние", max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Состояние"
        verbose_name_plural = "Состояния"


class RoomType(models.Model):
    name = models.CharField("Описание", max_length=50, unique=True)
    room_count = models.IntegerField("Количество комнат")

    def __str__(self):
        return f"{self.room_count} - {self.name}"

    class Meta:
        verbose_name = "Количество комнат"
        verbose_name_plural = "Количество комнат"


class Year(models.Model):
    year = models.PositiveSmallIntegerField(unique=True, verbose_name='год', default=timezone.now().year)

    def __str__(self):
        return f"{self.year}"

    class Meta:
        ordering = ["-year"]
        verbose_name = "Год"
        verbose_name_plural = "Года"


class Floor(models.Model):
    floor = models.IntegerField("Этаж")
    name = models.CharField("Описание", max_length=255, unique=True)

    def __str__(self):
        return f"{self.floor} - {self.name}"

    class Meta:
        ordering = ["floor"]
        verbose_name = "Этаж"
        verbose_name_plural = "Этажи"


class ObjectType(models.Model):
    name = models.CharField("Описание", max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Тип коммерческого объекта"
        verbose_name_plural = "Тип коммерческих объектов"


class RoomLocation(models.Model):
    name = models.CharField("Расположение", max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Расположение"
        verbose_name_plural = "Расположение"


class RealEstateAd(models.Model):
    AD_TYPE_CHOICES = (
        ('sell', 'продажа'),
        ('rent', 'аренда')
    )
    RENT_PERIOD_CHOICES = (
        ('hourly', 'почасовая'),
        ('daily', 'посуточно'),
        ('monthly', 'по месячно'),
        ('long_term', 'на долгий срок'),
    )
    public_id = models.CharField(
        primary_key=True,
        max_length=8,
        unique=True,
        editable=True,
        default=generate_short_id
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="пользователь",
        related_name="real_estate_ads",
    )
    is_approved = models.BooleanField(
        default=False,
        verbose_name='Подтвержденный',
        db_index=True
    )
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_ads',
        verbose_name='Подтвержден: '
    )
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Время подтверждения'
    )
    ad_type = models.CharField(
        max_length=255, choices=AD_TYPE_CHOICES, default="sell", verbose_name="тип сделки"
    )
    rent_period = models.CharField(
        max_length=255, blank=True, null=True, choices=RENT_PERIOD_CHOICES, verbose_name='период аренды'
    )
    ENI_code = models.CharField(max_length=14, verbose_name="код ЕНИ", blank=True, null=True)
    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        null=True,
        related_name='real_estate_region',
        verbose_name='регион'
    )
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        related_name='real_estate_city',
        verbose_name='город/село'
    )
    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='real_estate_district',
        verbose_name='район'
    )
    address = models.CharField(
        max_length=255, verbose_name="Адресс", null=True, blank=True, db_index=True
    )
    location = PointField(blank=True, null=True, srid=4326, verbose_name='Точка на карте'),
    latitude = models.DecimalField(
        max_digits=18,
        decimal_places=15,
        null=True,
        blank=True,
        verbose_name="Широта"
    )
    longitude = models.DecimalField(
        max_digits=17,
        decimal_places=14,
        null=True,
        blank=True,
        verbose_name="Долгота"
    )

    link_2gis = models.URLField(max_length=2048, blank=True, verbose_name='Ссылка 2gis')
    link_Youtube = models.URLField(max_length=2048, blank=True, verbose_name='Ссылка YouTube')
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True, db_index=True
    )
    is_active = models.BooleanField(
        default=False, verbose_name='Активный', db_index=True
    )
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.PROTECT,
        related_name='real_estate_ad_subscription',
        verbose_name='Срок рекламы',
        blank=True,
        null=True
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name=_('Премиум объявление')
    )
    view_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Количество просмотров'),
        db_index=True
    )
    telephone = models.ForeignKey(
        Telephone,
        on_delete=models.CASCADE,
        related_name='real_estate_telephone',
        verbose_name='телефония',
        blank=True,
        null=True
    )
    heating_type = models.ForeignKey(
        HeatingType,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="heating_type",
        verbose_name="отопление"
    )
    condition = models.ForeignKey(
        ConditionType,
        on_delete=models.SET_NULL,
        null=True,
        related_name="condition_type",
        verbose_name="состояние"
    )
    internet = models.ForeignKey(
        Internet,
        on_delete=models.CASCADE,
        related_name='real_estate_internet',
        verbose_name='интернет',
        blank=True,
        null=True
    )
    bathroom = models.ForeignKey(
        BathRoom,
        on_delete=models.CASCADE,
        related_name='real_estate_bath_room',
        verbose_name='санузел',
        blank=True,
        null=True
    )
    gas = models.ForeignKey(
        Gas,
        on_delete=models.CASCADE,
        related_name='real_estate_gs',
        verbose_name='газ',
        blank=True,
        null=True
    )
    balcony = models.ForeignKey(
        Balcony,
        on_delete=models.CASCADE,
        related_name='real_estate_balcony',
        verbose_name='балкон',
        blank=True,
        null=True
    )
    main_door = models.ForeignKey(
        MainDoor,
        on_delete=models.CASCADE,
        related_name='real_estate_main_door',
        verbose_name='входная дверь',
        blank=True,
        null=True
    )
    parking = models.ForeignKey(
        Parking,
        on_delete=models.CASCADE,
        related_name='real_estate_parking',
        verbose_name='парковка',
        blank=True,
        null=True
    )
    furniture = models.ForeignKey(
        Furniture,
        on_delete=models.CASCADE,
        related_name='real_estate_furniture',
        verbose_name='мебель',
        blank=True,
        null=True
    )
    floor_type = models.ForeignKey(
        FloorType,
        on_delete=models.CASCADE,
        related_name='real_estate_floor_type',
        verbose_name='пол',
        blank=True,
        null=True
    )
    ceiling_height = models.FloatField(
        verbose_name='высота потолков', blank=True, null=True
    )
    safety = models.ManyToManyField(
        Safety,
        related_name='real_estate_safety',
        verbose_name='безопасность',
        blank=True
    )
    other = models.ManyToManyField(
        Other,
        related_name='real_estate_other',
        verbose_name='разное',
        blank=True
    )
    document = models.ManyToManyField(
        Document,
        related_name='real_estate_document',
        verbose_name='документы',
        blank=True
    )
    description = models.TextField(
        verbose_name="описание", blank=True
    )
    qr_code = CloudinaryField(
        folder='real_estate/qr_codes/',
        transformation={'quality': 'auto:best'},
        verbose_name="QR-код",
        blank=True,
        null=True
    )
    price = models.DecimalField(
        verbose_name="цена", decimal_places=2, max_digits=10,
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.SET_NULL,
        null=True,
        related_name='real_estate_price_currency',
        verbose_name='валюта'
    )
    is_total_price = models.BooleanField(
        verbose_name="цена за всё", default=True
    )
    installment = models.BooleanField(verbose_name='возможность рассрочки', blank=True, null=True)
    mortgage = models.BooleanField(verbose_name='возможность ипотеки', blank=True, null=True)
    exchange = models.ForeignKey(
        Exchange,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="real_estate_exchange",
        verbose_name="тип обмена"
    )
    measurements_docs = models.FileField(
        verbose_name='обмеры',
        blank=True,
        null=True,
        upload_to='real_estate/documents/',
        storage=RawMediaCloudinaryStorage(),
        help_text='точные замеры'
    )
    designing_docs = models.FileField(
        verbose_name='дизайн',
        blank=True,
        null=True,
        upload_to='pdfs/',
        storage=RawMediaCloudinaryStorage(),
        help_text='архитектурное решение'
    )
    elevator = models.BooleanField(
        verbose_name='Лифт',
        blank=True,
        null=True
    )
    _qr_needs_regeneration = False

    def get_measurements_docs_url(self):
        if self.measurements_docs and self.is_active:
            return self.measurements_docs.url
        return None

    def get_designing_docs_url(self):
        if self.designing_docs and self.is_active:
            return self.designing_docs.url
        return None

    def clean(self):
        super().clean()
        if self.ad_type == 'rent' and not self.rent_period:
            raise ValidationError({'rent_period': 'Поле "rent_period" обязательно для аренды.'})
        if self.ad_type == 'sell' and self.rent_period:
            raise ValidationError({'rent_period': 'Поле "rent_period" должно быть пустым.'})

    def days_remaining(self):
        if self.subscription:
            expiration_date = self.approved_at + timedelta(days=self.subscription.duration_days)
            remaining = (expiration_date - timezone.now()).days
            return max(0, remaining)
        return 0

    @property
    def is_expired(self):
        return 0 >= self.days_remaining()

    def get_qr_url(self):
        pass

    def _generate_qr_code(self):
        try:
            qr_url = self.get_qr_url()
            qr_img = qrcode.make(qr_url)

            buffer = BytesIO()
            qr_img.save(buffer, format='PNG')
            buffer.seek(0)

            result = cloudinary.uploader.upload(
                buffer,
                public_id=f"qr_codes/{self.public_id}",
                format='png',
                overwrite=True
            )

            self.qr_code = result['public_id']
        except Exception as e:
            logger.error(f"Failed to generate QR code for {self.public_id}: {str(e)}")
            raise ValidationError("QR code generation failed. Please try again.")

    def regenerate_qr_code(self):
        self._qr_needs_regeneration = True
        self.save(update_fields=['qr_code'])

    def delete_qr_code(self):
        if self.qr_code:
            try:
                cloudinary.uploader.destroy(self.qr_code.public_id)
            except cloudinary.exceptions.NotFound:
                pass
            except Exception as e:
                logger.error(f"Failed to delete QR code {self.public_id}: {str(e)}")
                raise

            self.qr_code = None
            self.save(update_fields=['qr_code'])

    def set_location(self, lat, lon):
        from django.contrib.gis.geos import Point
        self.location = Point(lon, lat)
        self.latitude, self.longitude = lat, lon

    def save(self, *args, **kwargs):
        if not self.public_id:
            self.public_id = generate_short_id()

        if self._state.adding or self._qr_needs_regeneration:
            self._generate_qr_code()
            self._qr_needs_regeneration = False

        if self.is_expired:
            self.is_active = False
            self.is_approved = False
        elif self.is_approved:
            self.is_active = True

        else:
            self.latitude = None
            self.longitude = None

        super().save(*args, **kwargs)


class PhoneNumber(models.Model):
    ad = models.ForeignKey(
        RealEstateAd,
        on_delete=models.CASCADE,
        related_name='real_estate_phones',
        verbose_name='Объявление'
    )
    phone_regex = RegexValidator(
        regex=r'^\+996\d{9}$',
        message="Номер телефона должен начинаться с +996, за которым следуют 9 цифр. Пример: +996700123456"
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=13,
        verbose_name='телефон'
    )

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = 'Телефон'
        verbose_name_plural = 'Телефоны'


class RealEstateAdImage(models.Model):
    ad = models.ForeignKey(
        'RealEstateAd',
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Объявление'
    )
    image = CloudinaryField(
        folder='real_estate/',
        transformation={'quality': 'auto:low', 'fetch_format': 'auto'},
        verbose_name='Фотография'
    )
    is_main = models.BooleanField(
        default=False,
        verbose_name='Главное фото'
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата загрузки'
    )

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        ordering = ['-is_main', 'uploaded_at']

    def __str__(self):
        return f"Фото к объявлению #{self.ad.public_id}"

    def clean(self):
        if self.is_main and RealEstateAdImage.objects.filter(
            ad=self.ad,
            is_main=True
        ).exclude(pk=self.pk).exists():
            raise ValidationError('Может быть только одно главное фото.')