from datetime import timedelta

from django.contrib import admin
from django.contrib.gis.geos import Point
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django import forms

from applications.real_estate.models import RealEstateAd
from applications.real_estate_advertisement.models import (
    ApartmentAd, HouseAd, CommercialAd, RoomAd, PlotAd, DachaAd, ParkingAd
)
from applications.real_estate.admin import RealEstateAdImageInline, RealEstatePhoneNumberInline

from django.db.models import F, ExpressionWrapper, DurationField, fields

coord_validator = RegexValidator(
    r'^-?\d{1,3}\.\d{1,15}$',
    'Enter coordinates in -XXX.XXXXXXXXXXXXXX format'
)


class DaysRemainingFilter(admin.SimpleListFilter):
    title = 'Days Remaining'
    parameter_name = 'days_remaining'

    def lookups(self, request, model_admin):
        return (
            ('expired', 'Истек'),
            ('0_3', '0-3 дней'),
            ('3_7', '3-7 дней'),
            ('10_plus', '10+ дней'),
        )

    def queryset(self, request, queryset):
        now = timezone.now()

        queryset = queryset.annotate(
            expiration_date=ExpressionWrapper(
                F('created_at') + (F('subscription__duration_days') * timedelta(days=1)),
                output_field=fields.DateTimeField()
            ),
            days_left=ExpressionWrapper(
                F('expiration_date') - now,
                output_field=DurationField()
            )
        )

        if self.value() == 'expired':
            return queryset.filter(expiration_date__lte=now)
        elif self.value() == '0_3':
            return queryset.filter(
                expiration_date__gt=now,
                expiration_date__lte=now + timedelta(days=3)
            )
        elif self.value() == '3_7':
            return queryset.filter(
                expiration_date__gt=now + timedelta(days=3),
                expiration_date__lte=now + timedelta(days=7)
            )
        elif self.value() == '10_plus':
            return queryset.filter(expiration_date__gt=now + timedelta(days=10))
        return queryset


class RealEstateAdForm(forms.ModelForm):
    latitude = forms.DecimalField(
        widget=forms.HiddenInput(attrs={'id': 'id_latitude'}),
        required=False,
        max_digits=17,
        decimal_places=14
    )
    longitude = forms.DecimalField(
        widget=forms.HiddenInput(attrs={'id': 'id_longitude'}),
        required=False,
        max_digits=17,
        decimal_places=14
    )

    class Meta:
        model = RealEstateAd
        fields = '__all__'
        widgets = {
            'latitude': forms.HiddenInput(attrs={'id': 'id_latitude'}),
            'longitude': forms.HiddenInput(attrs={'id': 'id_longitude'}),
        }

    class Media:
        css = {
            'all': (
                'https://unpkg.com/leaflet-geosearch@3.6.1/dist/geosearch.css',
            )
        }
        js = (
            'admin/js/location_picker.js',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['latitude'].initial = self.instance.location.y if self.instance.location else None
            self.fields['longitude'].initial = self.instance.location.x if self.instance.location else None

    def save(self, commit=True):
        instance = super().save(commit=False)
        lat = self.cleaned_data.get('latitude')
        lng = self.cleaned_data.get('longitude')

        if lat and lng:
            # Update both location and decimal fields
            instance.location = Point(float(lng), float(lat))
            instance.latitude = lat
            instance.longitude = lng
        else:
            instance.location = None
            instance.latitude = None
            instance.longitude = None

        if commit:
            instance.save()
        return instance


class BaseRealEstateAdmin(admin.ModelAdmin):
    forms = RealEstateAdForm
    change_form_template = 'admin/property_change_form.html'
    inlines = [RealEstateAdImageInline, RealEstatePhoneNumberInline]
    list_display = [
        'public_id', 'price', 'days_remaining_display',
        'subscription', 'status_display', 'created_at', 'address', 'city', 'user',
        'is_approved', 'is_active', 'approved_by'
    ]
    list_editable = ('is_approved', 'is_active')
    list_display_links = ['public_id']
    list_filter = [
        DaysRemainingFilter, 'is_active', 'subscription',
    ]
    search_fields = [
        'public_id', 'title', 'description', 'user__email',
        'user__phone', 'address', 'city', 'district', 'region'
    ]
    actions = [
         'approve_ads', 'deactivate_ads'
    ]
    readonly_fields = ['user', 'is_active', 'public_id', 'created_at', 'updated_at',
                       'display_latitude', 'display_longitude', 'qr_preview', 'property_type', 'is_active', 'view_count',
                       ]
    autocomplete_fields = ['region', 'city', 'district', 'telephone']
    date_hierarchy = 'created_at'
    list_per_page = 20

    fieldsets = (
        (_('Основная информация'), {
            'fields': ('public_id', 'user', 'ad_type', 'property_type', 'title')
        }),
        (_('Расположение'), {
            'fields': ('region', 'city', 'district', 'link_2gis', 'address', 'latitude', 'longitude', )
        }),
        (_('Отображения'), {
            'fields': ('link_Youtube',)
        }),
        (_('Характеристики'), {
            'fields': ('elevator', 'telephone', 'heating_type', 'condition', 'internet', 'bathroom', 'gas', 'balcony',
                       'main_door', 'parking', 'furniture', 'floor_type', 'ceiling_height', 'safety', 'other',
                       'document', 'description', 'measurements_docs', 'designing_docs')
        }),
        (_('Цена и условия сделки'), {
            'fields': ('price', 'currency', 'price_kgs', 'is_total_price', 'exchange', 'installment', 'mortgage')
        }),
        (_('Статус объявления'), {
            'fields': ('subscription', 'is_featured', 'view_count', 'qr_code', )
        }),
    )

    def measurements_docs_link(self, obj):
        if obj.measurements_docs:
            return format_html('<a href="{}" target="_blank">View PDF</a>', obj.get_measurements_docs_url())
        return "No Measurement PDF attached"

    measurements_docs_link.short_description = 'Обмер объекта'

    def designing_docs_link(self, obj):
        if obj.designing_docs:
            return format_html('<a href="{}" target="_blank">View PDF</a>', obj.get_designing_docs_url())
        return "No Design PDF attached"

    designing_docs_link.short_description = 'Дизайн объекта'

    def status_display(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">✓ Активно</span>')
        return format_html('<span style="color: red;">✗ Неактивно</span>')

    status_display.short_description = _('Статус')

    @admin.action(description='Активировать выбранные объявления')
    def approve_ads(self, request, queryset):
        if not request.user.has_perm('realestate.can_approve_ads'):
            self.message_user(request, "У вас нет разрешения на одобрение рекламы", level='ERROR')
            return

        updated = queryset.update(
            is_approved=True,
            approved_by=request.user,
            approved_at=timezone.now(),
            is_active=True
        )
        self.message_user(request, f"{updated} ads approved")

    @admin.action(description='Деактивировать выбранные объявления')
    def deactivate_ads(self, request, queryset):
        if not request.user.has_perm('realestate.can_approve_ads'):
            self.message_user(request, "У вас нет разрешения на отключение рекламы", level='ERROR')
            return

        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} ads deactivated")

    def has_change_permission(self, request, obj=None):
        if obj and not request.user.has_perm('realestate.can_approve_ads'):
            return obj.user == request.user
        return super().has_change_permission(request, obj)

    def display_latitude(self, obj):
        return round(obj.latitude, 6) if obj.latitude else None

    def display_longitude(self, obj):
        return round(obj.longitude, 6) if obj.longitude else None

    map_width = 800
    map_height = 500

    class Media:
        css = {
            'all': ('https://unpkg.com/leaflet/dist/leaflet.css',)
        }
        js = ('admin/js/location_picker.js',)

    def qr_preview(self, obj):
        if obj.qr_code:
            return obj.qr_code.image(transformation={'width': 100, 'crop': 'fill'})
        return "-"

    qr_preview.allow_tags = True
    qr_preview.short_description = 'QR код'

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

    def days_remaining_display(self, obj):
        days = obj.days_remaining()
        if days <= 0:
            return 'Просрочен'
        return f'{days} дней'

    days_remaining_display.short_description = 'Истекают через: '

    def get_queryset(self, request):
        qs = super().get_queryset(request).select_related('user', 'city', 'district')
        if request.user.has_perm('realestate.can_approve_ads'):
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if 'is_approved' in form.changed_data and obj.is_approved:
            obj.approved_by = request.user
            obj.approved_at = timezone.now()

        lat = request.POST.get("latitude")
        lon = request.POST.get("longitude")

        if lat and lon:
            obj.location = Point(float(lon), float(lat))

        if not change or not obj.user_id:
            obj.user = request.user

        if obj.is_expired:
            obj.is_active = False

        super().save_model(request, obj, form, change)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if request.user.has_perm('realestate.can_approve_ads'):
            fieldsets += (
                ('Статус', {
                    'fields': ('is_approved', 'approved_by', 'approved_at', 'is_active')
                }),
            )
        return fieldsets


@admin.register(ApartmentAd)
class ApartmentAdAdmin(BaseRealEstateAdmin):
    fieldsets = BaseRealEstateAdmin.fieldsets + (
        (_('Тип объекта'), {
            'fields': ('rooms', 'residential_complex', 'series', 'building_type', 'construction_year', 'floor',
                       'max_floor', 'total_area', 'living_area', 'kitchen_area', 'ENI_code', 'rent_period')
        }),
    )
    list_filter = BaseRealEstateAdmin.list_filter + ['rooms', 'residential_complex', 'series', 'building_type', 'floor']
    search_fields = ('rooms', 'residential_complex')


@admin.register(HouseAd)
class HouseAdAdmin(BaseRealEstateAdmin):
    fieldsets = BaseRealEstateAdmin.fieldsets + (
        (_('Специфика дома'), {
            'fields': ('rooms', 'building_type', 'floor', 'area', 'total_area', 'ENI_code', 'rent_period')
        }),
    )
    list_filter = BaseRealEstateAdmin.list_filter + ['rooms', 'area', 'total_area']


@admin.register(CommercialAd)
class CommercialAdAdmin(BaseRealEstateAdmin):
    fieldsets = BaseRealEstateAdmin.fieldsets + (
        (_('Специфика коммерческой недвижимости'), {
            'fields': ('object_type', 'residential_complex', 'building_type', 'construction_year', 'floor',
                       'max_floor', 'total_area', 'ENI_code', 'rent_period')
        }),
    )
    list_filter = BaseRealEstateAdmin.list_filter + ['object_type', 'condition']


@admin.register(RoomAd)
class RoomAdAdmin(BaseRealEstateAdmin):
    fieldsets = BaseRealEstateAdmin.fieldsets + (
        (_('Специфика комнаты'), {
            'fields': ('rooms', 'room_location', 'floor', 'max_floor', 'total_area', 'ENI_code', 'rent_period')
        }),
    )
    list_filter = BaseRealEstateAdmin.list_filter + ['rooms', 'room_location']


@admin.register(PlotAd)
class PlotAdAdmin(BaseRealEstateAdmin):
    fieldsets = BaseRealEstateAdmin.fieldsets + (
        (_('Специфика участка'), {
            'fields': ('total_area', 'ENI_code', 'rent_period')
        }),
    )
    list_filter = BaseRealEstateAdmin.list_filter + ['total_area']


@admin.register(DachaAd)
class DachaAdAdmin(BaseRealEstateAdmin):
    fieldsets = BaseRealEstateAdmin.fieldsets + (
        (_('Специфика дачи'), {
            'fields': ('rooms', 'building_type', 'area', 'total_area', 'ENI_code', 'rent_period')
        }),
    )
    list_filter = BaseRealEstateAdmin.list_filter + ['area', 'total_area']


@admin.register(ParkingAd)
class ParkingAdAdmin(BaseRealEstateAdmin):
    fieldsets = BaseRealEstateAdmin.fieldsets + (
        (_('Специфика парковки'), {
            'fields': ('residential_complex', 'ENI_code', 'rent_period')
        }),
    )
    list_filter = BaseRealEstateAdmin.list_filter + ['residential_complex']
