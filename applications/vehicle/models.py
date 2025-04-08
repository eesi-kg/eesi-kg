from datetime import timedelta
from io import BytesIO

import qrcode
import cloudinary.uploader
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.timezone import now
from django.contrib.auth import get_user_model

from applications.common.models import Currency, Subscription, generate_short_id, Exchange, Region, City, CountryName
from applications.user.tasks import logger
from core import settings
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class VehicleAdManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'make', 'model', 'year', 'color', 'currency',
            'registration_country', 'other_info', 'exchange'
        ).prefetch_related(
            'appearance', 'salon', 'media', 'safety', 'option'
        )

    def active_vehicles(self):
        return self.filter(
            Q(is_active=True) &
            Q(subscription__isnull=False) &
            Q(created_at__gte=timezone.now() - timedelta(days=90))
        )

    def recent_vehicles(self, days=30):
        return self.filter(created_at__gte=timezone.now() - timedelta(days=days))


class VehicleCategory(models.TextChoices):
    passenger = ("passenger", _("легковые"))
    commercial = ("commercial", _("коммерческие"))
    special = ("special", _("спец.техника"))
    moto = ("moto", _("мотоциклы"))


class CommercialType(models.Model):
    name = models.CharField(verbose_name='тип', max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип коммерческих машин"
        verbose_name_plural = "Типы коммерческих машин"


class SpecialType(models.Model):
    name = models.CharField(verbose_name='тип', max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип спецтехники"
        verbose_name_plural = "Типы спецтехники"


class MotoType(models.Model):
    name = models.CharField(verbose_name='тип', max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип мото"
        verbose_name_plural = "Типы мото"


class Seria(models.Model):
    seria = models.CharField(verbose_name='Серия', unique=True)

    def __str__(self):
        return self.seria

    class Meta:
        verbose_name = "серия"
        verbose_name_plural = "серии"


class OtherInfo(models.Model):
    other_info = models.CharField(verbose_name='Прочее', unique=True)

    def __str__(self):
        return self.other_info

    class Meta:
        verbose_name = "прочее"
        verbose_name_plural = "прочее"


class Fuel(models.Model):
    fuel = models.CharField(verbose_name='Двигатель', unique=True)

    def __str__(self):
        return self.fuel

    class Meta:
        verbose_name = "двигатель"
        verbose_name_plural = "двигатели"


class Drive(models.Model):
    drive = models.CharField(verbose_name='Привод', unique=True)

    def __str__(self):
        return self.drive

    class Meta:
        verbose_name = "привод"
        verbose_name_plural = "приводы"


class Transmission(models.Model):
    transmission = models.CharField(verbose_name='Коробка передач', unique=True)

    def __str__(self):
        return self.transmission

    class Meta:
        verbose_name = "коробка передач"
        verbose_name_plural = "коробки передач"


class VehicleMake(models.Model):
    category = models.CharField(
        max_length=255, verbose_name=_('Название'), choices=VehicleCategory.choices
    )
    name = models.CharField(
        max_length=255, verbose_name=_('Название'), unique=True
    )
    country = models.ForeignKey(
        CountryName, blank=True, null=True, verbose_name=_('Страна'), on_delete=models.SET_NULL, related_name="make_country"
    )
    logo = models.ImageField(
        upload_to='vehicle_logos/', blank=True, null=True, verbose_name=_('Логотип')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Марка Транспорта')
        verbose_name_plural = _('Марки Транспорта')
        ordering = ['name']


class VehicleModel(models.Model):
    name = models.CharField(
        max_length=100, verbose_name=_('Название'), unique=True
    )
    make = models.ForeignKey(
        VehicleMake,
        on_delete=models.CASCADE,
        related_name='models',
        verbose_name=_('Марка')
    )
    picture = models.ImageField(upload_to='vehicle_model_details/', blank=True, null=True, verbose_name='картинка')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _('Модель')
        verbose_name_plural = _('Модели')
        ordering = ['name']


class VehicleModelImage(models.Model):
    model = models.ForeignKey(
        VehicleModel,
        on_delete=models.CASCADE,
        related_name='model_images',
        verbose_name=_('Транспортное средство')
    )
    image = models.ImageField(
        upload_to='model_images/',
        verbose_name=_('Изображение')
    )
    is_main = models.BooleanField(
        default=False,
        verbose_name=_('Основное изображение')
    )

    def __str__(self):
        return f"{_('Изображение для')} {self.model}"

    class Meta:
        verbose_name = _('Изображение')
        verbose_name_plural = _('Изображения')
        ordering = ['-is_main', ]


class VehicleYear(models.Model):
    year = models.PositiveIntegerField(verbose_name=_('Год выпуска'), unique=True)

    def __str__(self):
        return f"{self.year}"

    class Meta:
        verbose_name = _('Год выпуска')
        verbose_name_plural = _('Года выпусков')
        ordering = ['year']


class VehicleBodyType(models.Model):
    name = models.CharField(
        max_length=100, verbose_name=_('Название'), unique=True
    )
    icon = models.ImageField(
        upload_to='body_type_icons/', blank=True, null=True, verbose_name=_('Иконка')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Тип кузова')
        verbose_name_plural = _('Типы кузова')
        ordering = ['name']


class VehicleGeneration(models.Model):
    body_type = models.ForeignKey(
        VehicleBodyType,
        on_delete=models.CASCADE,
        related_name='body_type',
        verbose_name=_('Поколение')
    )
    name = models.CharField(
        max_length=100, verbose_name=_('Название'), unique=True
    )
    picture = models.ImageField(
        upload_to='vehicle_generation_pictures/', blank=True, null=True, verbose_name=_('Картинка')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Поколение')
        verbose_name_plural = _('Поколения')
        ordering = ['name']


class VehicleModification(models.Model):
    name = models.CharField(
        max_length=100, verbose_name=_('Название'), unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Модификация')
        verbose_name_plural = _('Модификации')
        ordering = ['name']


class VehicleColor(models.Model):
    color = models.CharField(
        max_length=100, verbose_name=_('Цвет'), unique=True
    )
    icon = models.ImageField(
        upload_to='color_icons/', blank=True, null=True, verbose_name=_('Цвета')
    )

    def __str__(self):
        return self.color

    class Meta:
        verbose_name = _('Цвет')
        verbose_name_plural = _('Цвета')
        ordering = ['color']


class Appearance(models.Model):
    name = models.CharField(
        max_length=255, verbose_name='Внешний вид', unique=True
    )
    icon = models.ImageField(
        upload_to='appearance_icons/', blank=True, null=True, verbose_name=_('Цвета')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Внешний вид')
        verbose_name_plural = _('Внешние виды')
        ordering = ['name']


class Salon(models.Model):
    name = models.CharField(
        max_length=255, verbose_name='Салон', unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Салон')
        verbose_name_plural = _('Салоны')
        ordering = ['name']


class Media(models.Model):
    name = models.CharField(
        max_length=255, verbose_name='Медиа', unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Медиа')
        verbose_name_plural = _('Медиа')
        ordering = ['name']


class Safety(models.Model):
    name = models.CharField(
        max_length=255, verbose_name='Безапасность', unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Безапасность')
        verbose_name_plural = _('Безапасность')
        ordering = ['name']


class Option(models.Model):
    name = models.CharField(
        max_length=255, verbose_name='Опции', unique=True
    )
    icon = models.ImageField(
        upload_to='color_icons/', blank=True, null=True, verbose_name=_('Цвета')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Опция')
        verbose_name_plural = _('Опции')
        ordering = ['name']


class VehicleAd(models.Model):
    CONDITION_CHOICES = (
        ('new', _('новое')),
        ('good', _('хорошее')),
        ('ideal', _('идеальное')),
        ('crushed', _('аварийное/не на ходу'))
    )
    AVAILABILITY_CHOICES = (
        ('in_stock', _('В наличии')),
        ('on_order', _('На заказ')),
        ('on_way', _('В пути')),
    )
    public_id = models.CharField(
        primary_key=True,
        max_length=8,
        unique=True,
        editable=False,
        default=generate_short_id
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='vehicles',
        verbose_name=_('Владелец объявления'),
        null=True,
        blank=True
    )
    make = models.ForeignKey(
        VehicleMake,
        on_delete=models.CASCADE,
        related_name='vehicles',
        verbose_name=_('Марка')
    )
    model = models.ForeignKey(
        VehicleModel,
        on_delete=models.CASCADE,
        related_name='vehicles',
        verbose_name=_('Модель')
    )
    year = models.ForeignKey(
        VehicleYear,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vehicle_year',
        verbose_name=_('Год выпуска')
    )
    color = models.ForeignKey(
        VehicleColor,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='vehicle_color',
        verbose_name='Цвет'
    )
    condition = models.CharField(
        max_length=10,
        choices=CONDITION_CHOICES,
        default='good',
        verbose_name=_('Состояние')
    )
    mileage = models.PositiveIntegerField(
        help_text=_("Пробег в километрах"),
        verbose_name=_('Пробег')
    )
    appearance = models.ManyToManyField(
        Appearance,
        blank=True,
        related_name='appearance',
        verbose_name=_('Внешний вид')
    )
    salon = models.ManyToManyField(
        Salon,
        blank=True,
        related_name='salon',
        verbose_name=_('Салон')
    )
    media = models.ManyToManyField(
        Media,
        blank=True,
        related_name='media',
        verbose_name=_('Медиа')
    )
    safety = models.ManyToManyField(
        Safety,
        blank=True,
        related_name='safety',
        verbose_name=_('Безапасность')
    )
    option = models.ManyToManyField(
        Option,
        blank=True,
        related_name='option',
        verbose_name=_('Опция')
    )
    description = models.TextField(
        blank=True, null=True, verbose_name=_('Описание')
    )
    availability_in_KG = models.CharField(
        max_length=10,
        choices=AVAILABILITY_CHOICES,
        default='in_stock',
        verbose_name=_('Наличие в Кыргызстане')
    )
    cleared_in_KG = models.BooleanField(
        default=True, verbose_name=_('Расстаможен в Кыргызстане')
    )
    registration_country = models.ForeignKey(
        CountryName,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='country_registration',
        verbose_name=_('Страна регистрации')
    )
    other_info = models.ForeignKey(
        OtherInfo,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='vehicle_other_info',
        verbose_name=_('Прочее')
    )
    vin = models.CharField(
        max_length=17,
        blank=True,
        null=True,
        verbose_name=_('VIN-код')
    )
    plate = models.CharField(
        max_length=12,
        blank=True,
        null=True,
        verbose_name=_('Гос номер авто')
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_('Цена')
    )
    currency = models.ForeignKey(
        Currency,
        verbose_name=_('Валюта'),
        on_delete=models.SET_NULL,
        null=True,
        related_name='vahicle_ad_currency'
    )
    exchange = models.ForeignKey(
        Exchange,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Возможность обмена')
    )
    installment_payment = models.BooleanField(
        default=False,
        verbose_name=_('Возможность рассрочки')
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name=_('Премиум объявление')
    )
    view_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Количество просмотров')
    )
    last_updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_vehicles',
        verbose_name=_('Последнее обновление пользователем')
    )
    link_Youtube = models.URLField(max_length=2048, blank=True, verbose_name='Ссылка YouTube')
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True
    )
    updated_at = models.DateTimeField(
        auto_now=True, db_index=True
    )
    is_active = models.BooleanField(
        default=False, verbose_name='активный', db_index=True
    )
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.PROTECT,
        related_name='vehicle_ad_subscription',
        verbose_name='подписка',
        blank=True,
        null=True
    )
    qr_code = CloudinaryField(
        folder='vehicle/qr_codes/',
        transformation={'quality': 'auto:best'},
        verbose_name="QR-код",
        blank=True,
        null=True
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        null=True,
        related_name='vehicle_region',
        verbose_name='регион'
    )
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        related_name='vehicle_city',
        verbose_name='город/село'
    )

    _qr_needs_regeneration = False

    def expiration_date(self):
        if self.subscription:
            return self.created_at + timedelta(days=self.subscription.duration_days)
        return self.created_at  # или None

    def is_expired(self):
        return self.subscription and now() > self.expiration_date

    def get_qr_url(self):
        base_url = getattr(settings, 'QR_BASE_URL')
        return f"{base_url}/real-estate/{self.public_id}/"

    def _generate_qr_code(self):
        """Internal method for QR code generation with error handling"""
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
                overwrite=True  # Important for updates
            )

            self.qr_code = result['public_id']
        except Exception as e:
            logger.error(f"Failed to generate QR code for {self.public_id}: {str(e)}")
            raise ValidationError("QR code generation failed. Please try again.")

    def regenerate_qr_code(self):
        """Explicit method for QR code regeneration"""
        self._qr_needs_regeneration = True
        self.save(update_fields=['qr_code'])

    def delete_qr_code(self):
        """Safe QR code deletion with cleanup"""
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

    def save(self, *args, **kwargs):
        if self._state.adding or self._qr_needs_regeneration:
            self._generate_qr_code()
            self._qr_needs_regeneration = False
        if self.subscription:
            self.is_active = True
        else:
            self.is_active = False
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Транспортное средство')
        verbose_name_plural = _('Транспортные средства')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['make', 'model']),
            models.Index(fields=['is_active', 'created_at']),
            models.Index(fields=['price']),
            models.Index(fields=['year', 'city']),
            models.Index(fields=['user']),
        ]

    def increment_view(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])

    def deactivate(self):
        self.status = 'dactivated'
        self.save(update_fields=['status'])

    def activate(self):
        self.status = 'active'
        self.save(update_fields=['status'])

    def __str__(self):
        return f"{self.make.name} {self.model.name} {self.year}"


class VehicleImage(models.Model):
    vehicle = models.ForeignKey(
        VehicleAd,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_('Транспортное средство')
    )
    image = CloudinaryField(
        folder='vehicle_images/',
        transformation={'quality': 'auto:low', 'fetch_format': 'auto'},
        verbose_name=_('Изображение')
    )
    is_main = models.BooleanField(
        default=False,
        verbose_name=_('Основное изображение')
    )

    def __str__(self):
        return f"{_('Изображение для')} {self.vehicle}"

    class Meta:
        verbose_name = _('Изображение')
        verbose_name_plural = _('Изображения')
        ordering = ['-is_main', ]

    def clean(self):
        # Validation to ensure only one main image per vehicle
        if self.is_main and VehicleImage.objects.filter(vehicle=self.vehicle, is_main=True).exclude(
                pk=self.pk).exists():
            raise ValidationError(_('Может быть только одно основное изображение для транспортного средства.'))


class PhoneNumber(models.Model):
    ad = models.ForeignKey(
        VehicleAd,
        on_delete=models.CASCADE,
        related_name='vehicle_phones',
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


class Attribute(models.Model):
    name = models.CharField("Название атрибута", max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Атрибут"
        verbose_name_plural = "Атрибуты"


class VehicleModelDetail(models.Model):
    vehicle_model = models.ForeignKey(
        VehicleModel,
        on_delete=models.CASCADE,
        related_name="vehicle_model_detail",
        verbose_name="характеристики",
        null=True,
        blank=True
    )
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, verbose_name="Атрибут", blank=True, null=True, related_name="attributes")
    value_string = models.CharField(max_length=255, null=True, blank=True, verbose_name="Значение")

    def __str__(self):
        return f"{self.attribute}: {self.value_string}"

    class Meta:
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"








