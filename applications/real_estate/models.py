from datetime import timedelta

import qrcode
import cloudinary.uploader
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from django.contrib.gis.db.models import PointField

from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from qrcode.image.styledpil import StyledPilImage

from applications.common.models import Currency, Exchange, Region, City, District, \
    generate_short_id, Subscription, ExchangeRate
from django.contrib.auth import get_user_model

from django.db import models
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField

from applications.user.tasks import logger
from django.core.cache import cache

import logging

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

from decimal import Decimal

User = get_user_model()

logger = logging.getLogger(__name__)


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
    CURRENCY_CHOICES = [
        ('USD', 'Доллар США'),
        ('KGS', 'Кыргызский сом'),
    ]
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
        validators=[
            MinValueValidator(-90),
            MaxValueValidator(90)
        ],
        null=True,
        blank=True,
        verbose_name="Широта"
    )
    longitude = models.DecimalField(
        max_digits=17,
        decimal_places=14,
        validators=[
            MinValueValidator(-180),
            MaxValueValidator(180)
        ],
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
    qr_code = models.URLField(
        max_length=900,  # Увеличиваем максимальную длину для URL
        verbose_name="QR-код PDF",
        blank=True,
        null=True
    )
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='USD',
        verbose_name="Валюта"
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Цена"
    )
    price_kgs = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Цена в сомах",
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
        if self.subscription and self.approved_at:
            expiration_date = self.approved_at + timedelta(days=self.subscription.duration_days)
            remaining = (expiration_date - timezone.now()).days
            return max(0, remaining)
        return 0

    @property
    def is_expired(self):
        return 0 >= self.days_remaining()

    def get_qr_url(self):
        cache_key = f'real_estate_qr_url_{self.public_id}'
        url = cache.get(cache_key)
        
        if url is None:
            url = self._generate_qr_url()
            cache.set(cache_key, url, timeout=3600)  # кэшируем на час
        
        return url

    def _get_property_display_text(self):
        """Получаем текст с правильным склонением"""
        try:
            texts = ["ПРОДАЮ" if self.ad_type == 'sell' else "СДАЮ"]
            # Комнаты и тип недвижимости в правильном склонении
            if self.property_type == 'apartments':
                room_text = f"{self.rooms.room_count}-КОМН." if hasattr(self, 'rooms') and self.rooms else ""
                texts.append(room_text)
                texts.append("КВАРТ.")
            elif self.property_type == 'houses':
                room_text = f"{self.rooms.room_count}-КОМН." if hasattr(self, 'rooms') and self.rooms else ""
                texts.append(room_text)
                texts.append("ДОМ")
            elif self.property_type == 'commercials':
                object_type = f"{self.object_type.name}" if hasattr(self, 'object_type') else "КОММ. ПОМ."
                texts.append(object_type)
            elif self.property_type == 'plots':
                texts.append("УЧАСТОК")
            elif self.property_type == 'dachas':
                texts.append("ДАЧУ")
            elif self.property_type == 'parkings':
                texts.append("ПАРКИНГ")
            
            if hasattr(self, 'total_area') and self.total_area:
                if self.property_type == 'plots':
                    texts.append(f"{int(self.total_area)} СОТ.")
                else:
                    texts.append(f"{int(self.total_area)} m²")
            
            return texts
        except Exception as e:
            logger.error(f"Error in _get_property_display_text: {str(e)}")
            return ["ОБЪЯВЛЕНИЕ"]

    def _generate_qr_code_pdf(self):
        try:
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            from reportlab.lib.styles import ParagraphStyle
            from reportlab.platypus import Paragraph
            
            # Регистрируем шрифт
            font_path = 'templates/fonts/Arial Bold.ttf'
            pdfmetrics.registerFont(TTFont('ArialBold', font_path))
            
            # Создаем PDF
            buffer = BytesIO()
            width, height = A4[1], A4[0]  # Альбомная ориентация
            
            pdf = canvas.Canvas(buffer, pagesize=(width, height))
            pdf._doc.setProducer('eesi.kg PDF Generator')
            pdf._doc.setAuthor('eesi.kg')
            
            # Желтый фон
            pdf.setFillColor(colors.HexColor('#FFD700'))
            pdf.rect(0, 0, width, height, fill=True)
            
            # QR код размеры и позиция
            qr_size = 400
            qr_x = width - qr_size - 60
            qr_y = (height - qr_size) // 2
            
            # Создаем QR код
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=12,
                border=2,
            )
            qr.add_data(self.get_qr_url())
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")
            
            # Единый стиль для всего текста
            style = ParagraphStyle(
                'UnifiedStyle',
                fontName='ArialBold',
                fontSize=55,
                leading=60,
                alignment=0,
                textColor=colors.white,
                spaceAfter=0,
            )
            
            # Получаем текст для отображения
            display_texts = self._get_property_display_text()
            
            # Расчет позиций для точного выравнивания по высоте QR кода
            num_lines = len([text for text in display_texts if text.strip()])
            line_height = qr_size / num_lines  # Равномерно распределяем по высоте QR кода
            
            # Отрисовка текста
            left_margin = 60
            available_width = qr_x - left_margin - 50
            
            # Начинаем с того же уровня, где начинается QR код
            y_position = qr_y + qr_size  # Начальная позиция совпадает с верхней границей QR кода
            
            for text in display_texts:
                if text.strip():
                    p = Paragraph(text.encode('utf-8').decode('utf-8'), style)
                    w, h = p.wrap(available_width, line_height)
                    p.drawOn(pdf, left_margin, y_position - h)  # Отрисовываем текст
                    y_position -= line_height  # Смещаемся вниз на высоту строки
            
            # Логотип
            pdf.setFont('ArialBold', 55)
            pdf.setFillColor(colors.white)
            logo_text = 'eesi.kg'.encode('utf-8').decode('utf-8')
            pdf.drawString(left_margin, 50, logo_text)
            
            # Белый фон под QR код
            pdf.setFillColor(colors.white)
            pdf.rect(qr_x - 10, qr_y - 10, qr_size + 20, qr_size + 20, fill=True)
            
            # Размещаем QR код
            qr_buffer = BytesIO()
            qr_img.save(qr_buffer, format='PNG')
            qr_buffer.seek(0)
            pdf.drawImage(ImageReader(qr_buffer), qr_x, qr_y, width=qr_size, height=qr_size)
            
            # Инструкция для QR кода
            pdf.setFont('ArialBold', 14)
            instruction = "наведите камеру на QR-код, чтобы открыть объявление"
            instruction = instruction.encode('utf-8').decode('utf-8')
            text_width = pdf.stringWidth(instruction, 'ArialBold', 14)
            x_position = qr_x + (qr_size - text_width) / 2
            pdf.drawString(x_position, qr_y + qr_size + 25, instruction)
            
            # Сохраняем PDF
            pdf.save()
            buffer.seek(0)
            
            # Загружаем в Cloudinary
            result = cloudinary.uploader.upload(
                buffer,
                resource_type="raw",
                public_id=f"qr_codes/{self.public_id}",
                format="pdf",
                overwrite=True,
                type="upload",
                access_mode="public",
                use_filename=True,
                unique_filename=False,
                content_type="application/pdf"
            )
            
            self.qr_code = result['secure_url']
            self._qr_needs_regeneration = False
            
        except Exception as e:
            logger.error(f"Failed to generate QR code PDF for {self.public_id}: {str(e)}")
            raise ValidationError(f"QR code PDF generation failed: {str(e)}")

    def get_qr_pdf_url(self):
        """Получить URL PDF файла с QR кодом"""
        if self.qr_code and self.is_active:
            return self.qr_code  # Теперь просто возвращаем сохраненный URL
        return None

    def set_location(self, lat, lon):
        """Установка координат"""
        from django.contrib.gis.geos import Point
        if lat is not None and lon is not None:
            self.location = Point(float(lon), float(lat))
            self.latitude = lat
            self.longitude = lon
            
    def calculate_price_kgs(self):
        """Calculate price in KGS based on current exchange rate"""
        try:
            exchange_rate = ExchangeRate.objects.latest('updated_at')
            if self.currency == 'USD':
                self.price_kgs = self.price * exchange_rate.rate
            else:
                self.price_kgs = self.price
        except ExchangeRate.DoesNotExist:
            # If no exchange rate is set, keep the existing value
            pass

    def save(self, *args, **kwargs):
        if self.is_approved and self.approved_at:
            self.is_active = True
        
        if self.is_expired:
            self.is_active = False
            self.is_approved = False

        if self.latitude and self.longitude and not self.location:
            self.set_location(self.latitude, self.longitude)
        
        is_new = not self.pk or self._qr_needs_regeneration
        # Проверяем, был ли удален QR код
        if self.pk:
            old_instance = RealEstateAd.objects.get(pk=self.pk)
            if old_instance.qr_code and not self.qr_code:
                self._qr_needs_regeneration = True
        
        super().save(*args, **kwargs)
        
        # Генерируем QR код если нужно
        if self._qr_needs_regeneration or not self.qr_code:
            self._generate_qr_code_pdf()
            if not kwargs.get('update_fields'):
                super().save(update_fields=['qr_code'])

        if self.is_approved and self.approved_at:
            self.is_active = True
        
        if self.is_expired:
            self.is_active = False
            self.is_approved = False
        elif self.is_approved:
            self.is_active = True

        if self.latitude and self.longitude and not self.location:
            self.set_location(self.latitude, self.longitude)
        
        cache_keys = [
            f'real_estate_list_{self.ad_type}',
            f'real_estate_detail_{self.public_id}'
        ]
        cache.delete_many(cache_keys)
        self.calculate_price_kgs()
        super().save(*args, **kwargs)

    def delete_qr_code(self):
        """Метод для удаления QR кода"""
        if self.qr_code:
            try:
                # Получаем public_id из URL
                public_id = self.qr_code.split('/')[-1].split('.')[0]
                cloudinary.uploader.destroy(f"qr_codes/{public_id}", resource_type="raw")
                self.qr_code = None
                self.save(update_fields=['qr_code'])
            except Exception as e:
                logger.error(f"Failed to delete QR code for {self.public_id}: {str(e)}")

    def get_price_display(self):
        """Метод для отображения цены в обеих валютах"""
        if self.currency == 'USD' and self.price_kgs:
            return f"{int(self.price)} USD / {int(self.price_kgs)} KGS"
        elif self.currency == 'KGS' and self.price:
            return f"{int(self.price)} KGS"
        return f"{int(self.price)} {self.currency}"

    class Meta:
        indexes = [
            models.Index(fields=['ad_type', 'is_active']),
            models.Index(fields=['created_at', 'is_active']),
            models.Index(fields=['price', 'currency']),
            models.Index(fields=['city', 'district']),       
        ]


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


class MarketingImage(models.Model):
    PROPERTY_TYPE_CHOICES = (
        ('apartments', 'Квартиры'),
        ('houses', 'Дома'),
        ('commercials', 'Коммерческая недвижимость'),
        ('rooms', 'Комнаты'),
        ('plots', 'Участки'),
        ('dachas', 'Дачи'),
        ('parkings', 'Паркинги'),
    )

    image = CloudinaryField(
        folder='marketing/',
        transformation={'quality': 'auto:low', 'fetch_format': 'auto'},
        verbose_name='Рекламное изображение'
    )
    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPE_CHOICES,
        verbose_name='Тип недвижимости'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активно'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Рекламное изображение'
        verbose_name_plural = 'Рекламные изображения'
        ordering = ['-created_at']

    def __str__(self):
        return f"Реклама для {self.get_property_type_display()}"