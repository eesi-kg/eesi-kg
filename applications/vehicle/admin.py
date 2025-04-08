from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import (VehicleMake, VehicleModel, VehicleYear, VehicleBodyType,
                     VehicleGeneration, VehicleModification, VehicleColor, Appearance, Salon,
                     Media, Safety, Option, VehicleImage, Seria, Fuel, Drive, Transmission,
                     PhoneNumber, OtherInfo, Attribute, VehicleModelDetail, VehicleModelImage
                     )
from ..vehicle_advertisement.models import CommercialType, MotoType, SpecialType

User = get_user_model()


@admin.register(CommercialType)
class VehicleCommercialTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(SpecialType)
class VehicleSpecialTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(MotoType)
class VehicleMotoTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class VehicleModelImageInline(admin.TabularInline):
    model = VehicleModelImage
    extra = 3


class VehicleImageInline(admin.TabularInline):
    model = VehicleImage
    extra = 1
    fields = ('image', 'is_main',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        return obj.image.build_html(width=100, crop="fill") if obj.image else ""

    image_preview.short_description = _('Предпросмотр')


class VehiclePhoneNumberInline(admin.TabularInline):
    model = PhoneNumber
    extra = 1


class VehicleModelInline(admin.TabularInline):
    model = VehicleModel
    extra = 1
    fields = ('name',)


@admin.register(VehicleMake)
class VehicleMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'logo_preview', 'model_count')
    search_fields = ('name', 'country')
    inlines = [VehicleModelInline]

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="40" height="auto" />', obj.logo.url)
        return "No Logo"

    logo_preview.short_description = _('Логотип')

    def model_count(self, obj):
        return obj.models.count()

    model_count.short_description = _('Количество моделей')


@admin.register(VehicleYear)
class VehicleYearAdmin(admin.ModelAdmin):
    list_display = ('year',)
    search_fields = ('year',)


@admin.register(OtherInfo)
class OtherInfoAdmin(admin.ModelAdmin):
    list_display = ('other_info',)
    search_fields = ('other_info',)


@admin.register(VehicleBodyType)
class VehicleBodyTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_preview')
    search_fields = ('name',)

    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="40" height="auto" />', obj.icon.url)
        return "No Icon"

    icon_preview.short_description = _('Иконка')


@admin.register(VehicleGeneration)
class VehicleGenerationAdmin(admin.ModelAdmin):
    list_display = ('name', 'body_type', 'picture_preview')
    list_filter = ('body_type',)
    search_fields = ('name',)

    def picture_preview(self, obj):
        if obj.picture:
            return format_html('<img src="{}" width="60" height="auto" />', obj.picture.url)
        return "No Picture"

    picture_preview.short_description = _('Картинка')


@admin.register(Seria)
class VehicleSeriaAdmin(admin.ModelAdmin):
    list_display = ('seria',)
    search_fields = ('seria',)


@admin.register(Fuel)
class VehicleFuelAdmin(admin.ModelAdmin):
    list_display = ('fuel',)
    search_fields = ('fuel',)


@admin.register(Drive)
class VehicleDriveAdmin(admin.ModelAdmin):
    list_display = ('drive',)
    search_fields = ('drive',)


@admin.register(Transmission)
class VehicleTransmissionAdmin(admin.ModelAdmin):
    list_display = ('transmission',)
    search_fields = ('transmission',)


@admin.register(VehicleModification)
class VehicleModificationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(VehicleColor)
class VehicleColorAdmin(admin.ModelAdmin):
    list_display = ('color', 'color_preview')
    search_fields = ('color',)

    def color_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="30" height="auto" />', obj.icon.url)
        return "No Color"

    color_preview.short_description = _('Цвет')


@admin.register(Appearance)
class AppearanceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Safety)
class SafetyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class UserAdmin(admin.ModelAdmin):
    search_fields = ['username', 'email', 'phone']


class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)


admin.site.register(Attribute, AttributeAdmin)


class VehicleModelDetailInline(admin.TabularInline):
    model = VehicleModelDetail
    extra = 1


@admin.register(VehicleModel)
class VehicleModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'make', )
    list_filter = ('make',)
    search_fields = ('name', 'make__name')
    inlines = (VehicleModelDetailInline, VehicleModelImageInline)

    def get_attributes(self, obj):
        return ", ".join([str(attr) for attr in obj.engineattribute_set.all()])

    get_attributes.short_description = "Атрибуты"
