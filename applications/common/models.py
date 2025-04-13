import shortuuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


def generate_short_id():
    return shortuuid.ShortUUID().random(length=8)


class Subscription(models.Model):
    duration_days = models.PositiveIntegerField(
        default=30,
        verbose_name='Длительность объявления'
    )
    days_before_notification = models.PositiveSmallIntegerField(
        default=3,
        verbose_name='Количество дней перед уведомлением'
    )
    price = models.DecimalField(
        verbose_name="Цена в день",
        decimal_places=2,
        max_digits=10,
        default=0
    )
    discount = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Скидка в %',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    def get_price(self) -> Decimal:
        discount_decimal = Decimal(self.discount) / Decimal(100)
        total = (Decimal(self.duration_days) * self.price) * (Decimal(1) - discount_decimal)
        return total.quantize(Decimal('0.00'))

    def __str__(self) -> str:
        return f'{self.duration_days} дней - {self.get_price()} сом' \
            if self.discount == 0 else (f'{self.duration_days} дней со скидкой {self.discount} % '
                                        f'- {self.get_price()} сом')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Region(models.Model):
    region = models.CharField(max_length=255, verbose_name='Область', unique=True)
    ordering = models.PositiveIntegerField(verbose_name="Очередность", blank=True, null=True)

    def __str__(self):
        return self.region

    class Meta:
        ordering = ["ordering", "region"]
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"


class City(models.Model):
    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        null=True,
        related_name="city_region",
        verbose_name="Регион"
    )
    city = models.CharField(max_length=255, verbose_name="Город", unique=True)
    ordering = models.PositiveIntegerField(verbose_name="Очередность", blank=True, null=True)

    def __str__(self):
        return f"{self.region} / {self.city}"

    class Meta:
        ordering = ["ordering", "region"]
        verbose_name = "Город"
        verbose_name_plural = "Города"


class District(models.Model):
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        related_name="district_city",
        verbose_name="Район"
    )
    district = models.CharField(max_length=255, verbose_name="Район", unique=True)
    ordering = models.PositiveIntegerField(verbose_name="Очередность", blank=True, null=True)

    def __str__(self):
        return f"{self.city} / {self.district}"

    class Meta:
        ordering = ["ordering", "district"]
        verbose_name = "Район"
        verbose_name_plural = "Район"


class Currency(models.Model):
    CURRENCY_CHOICES = (
        ('KGS', _('сом')),
        ('USD', _('дол. США'))
    )
    currency = models.CharField(max_length=255, verbose_name='валюта', choices=CURRENCY_CHOICES,)
    logo = models.ImageField(upload_to='currency_logos/', blank=True, null=True, verbose_name="эмблема")

    def __str__(self):
        return self.currency

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'


class Exchange(models.Model):
    exchange_type = models.CharField(max_length=255, verbose_name="тип обмена")

    def __str__(self):
        return self.exchange_type

    class Meta:
        verbose_name = 'Тип обмена'
        verbose_name_plural = 'Типы обмена'


class CountryName(models.Model):
    name = models.CharField(
        max_length=255, verbose_name='Страна', unique=True
    )
    flag = models.ImageField(blank=True, null=True, verbose_name="Флаг", upload_to="country_flags/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Страна')
        verbose_name_plural = _('Страны')
        ordering = ['name']
        

class ExchangeRate(models.Model):
    """Модель для хранения курса валют"""
    rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Курс USD к KGS",
        help_text="Текущий курс доллара к сому"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        verbose_name = "Курс валюты"
        verbose_name_plural = "Курсы валют"

    def __str__(self):
        return f"1 USD = {self.rate} KGS (обновлено: {self.updated_at.strftime('%d.%m.%Y %H:%M')})"

    @classmethod
    def get_current_rate(cls):
        """Получить текущий курс валюты"""
        return cls.objects.latest('updated_at').usd_to_kgs