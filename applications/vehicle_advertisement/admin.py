from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from applications.vehicle.admin import VehicleImageInline, VehiclePhoneNumberInline
from applications.vehicle_advertisement.models import (
    PassengerCar, CommercialCar, SpecialCar, Moto
)


class PriceRangeFilter(admin.SimpleListFilter):
    title = _('Ценовой диапазон')
    parameter_name = 'price_range'

    def lookups(self, request, model_admin):
        return (
            ('low', _('До 10,000 сом')),
            ('medium', _('10,000 - 50,000 сом')),
            ('high', _('50,000 - 100,000 сом')),
            ('premium', _('Свыше 100,000 сом')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(price__lt=10000, currency='KGS')
        if self.value() == 'medium':
            return queryset.filter(price__gte=10000, price__lt=50000, currency='KGS')
        if self.value() == 'high':
            return queryset.filter(price__gte=50000, price__lt=100000, currency='KGS')
        if self.value() == 'premium':
            return queryset.filter(price__gte=100000, currency='KGS')


class BaseVehicleAdmin(admin.ModelAdmin):
    list_display = (
        'public_id', 'user', 'make_model_year', 'price_display', 'condition', 'created_at', 'is_active', 'view_count')
    list_filter = ['condition', 'make', 'model', 'year', PriceRangeFilter]
    search_fields = (
        'user__email', 'user__username', 'vin', 'plate', 'make__name', 'model__name')
    readonly_fields = ('public_id', 'view_count', 'created_at', 'updated_at')
    fieldsets = (
        (_('Основная информация'), {
            'fields': ('public_id', 'title', 'category'),
        }),
        (_('Технические характеристики'), {
            'fields': ('make', 'model', 'year',),
        }),
        (_('Комплектация'), {
            'fields': (
                'color', 'condition', 'mileage', 'appearance', 'salon', 'media', 'safety', 'option', 'description'),
        }),
        (_('Дополнительная информация'), {
            'fields': ('availability_in_KG', 'cleared_in_KG', 'registration_country', 'other_info'),
        }),
        (_('Гос номер и VIN номер кузова'), {
            'fields': ('vin', 'plate',),
        }),
        (_('Цена и условия'), {
            'fields': ('price', 'currency', 'exchange', 'installment_payment'),
        }),
        (_('Медиа'), {
            'fields': ('link_Youtube',),
        }),
        (_('Расположение'), {
            'fields': (
                'region', 'city',)
        }),
        (_('Администрирование'), {
            'fields': (
                'is_featured', 'view_count', 'created_at', 'updated_at', 'subscription', 'qr_code'),
        }),
    )
    inlines = [VehicleImageInline, VehiclePhoneNumberInline]
    actions = ['deactivate_vehicles', 'activate_vehicles']
    autocomplete_fields = ['user', 'make', 'model', 'year']
    list_per_page = 20
    date_hierarchy = 'created_at'

    def make_model_year(self, obj):
        if hasattr(obj.year, 'year'):
            year_display = obj.year.year
        else:
            year_display = str(obj.year)
        return f"{obj.make.name} {obj.model.name} ({year_display})"

    make_model_year.short_description = _('Марка/Модель/Год')

    def price_display(self, obj):
        return f"{obj.price:,} {obj.currency}"

    price_display.short_description = _('Цена')

    def deactivate_vehicles(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, _('%(count)d объявлений деактивированы.') % {'count': updated})

    deactivate_vehicles.short_description = _('Деактивировать объявления')

    def activate_vehicles(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, _('%(count)d объявлений активированы.') % {'count': updated})

    activate_vehicles.short_description = _('Активировать объявления')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related(
            'user', 'make', 'model', 'year',
        ).prefetch_related('images')
        return queryset


@admin.register(PassengerCar)
class PassengerCarAdmin(BaseVehicleAdmin):
    fieldsets = BaseVehicleAdmin.fieldsets + (
        (_('Технические характеристики'), {
            'fields': (
                'body_type', 'generation', 'fuel_type', 'drive_type', 'transmission', 'modification', 'steering',)
        }),
    )
    list_filter = BaseVehicleAdmin.list_filter + ['body_type', 'generation', 'fuel_type', 'drive_type', 'transmission',
                                                  'steering']
    search_fields = ('body_type', 'generation', 'fuel_type', 'drive_type')


@admin.register(CommercialCar)
class CommercialCarAdmin(BaseVehicleAdmin):
    fieldsets = BaseVehicleAdmin.fieldsets + (
        (_('Технические характеристики'), {
            'fields': (
                'commercial_type', 'body_type', 'generation', 'fuel_type', 'drive_type', 'transmission', 'modification',
                'steering',)
        }),
    )
    list_filter = BaseVehicleAdmin.list_filter + ['commercial_type', 'body_type', 'generation', 'fuel_type',
                                                  'drive_type',
                                                  'transmission', 'steering']
    search_fields = ('commercial_type', 'body_type', 'generation', 'fuel_type', 'drive_type')


@admin.register(SpecialCar)
class SpecialCarAdmin(BaseVehicleAdmin):
    fieldsets = BaseVehicleAdmin.fieldsets + (
        (_('Технические характеристики'), {
            'fields': (
                'special_type', 'fuel_type', 'steering',)
        }),
    )
    list_filter = BaseVehicleAdmin.list_filter + ['fuel_type', 'steering']
    search_fields = ('fuel_type', 'steering')


@admin.register(Moto)
class MotoAdmin(BaseVehicleAdmin):
    fieldsets = BaseVehicleAdmin.fieldsets + (
        (_('Технические характеристики'), {
            'fields': (
                'moto_type', 'seria', 'modification',)
        }),
    )
    list_filter = BaseVehicleAdmin.list_filter + ['seria', 'modification']
    search_fields = ('seria', 'modification')
