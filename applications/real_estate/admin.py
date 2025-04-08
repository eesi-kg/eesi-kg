from django.contrib import admin

from .models import (Floor, Series, ResidentialComplex, RoomType, BuildingType, Year, RealEstateAdImage,
                     ConditionType, HeatingType, Developer, PhoneNumber, District, ObjectType,
                     RoomLocation, Telephone, Internet, BathRoom, Gas, Balcony, MainDoor, Parking, Furniture, FloorType,
                     Safety, Other, Document, Exchange, )


class RealEstateAdImageInline(admin.TabularInline):
    model = RealEstateAdImage
    extra = 1
    fields = ('image', 'is_main', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        return obj.image.build_html(width=100, crop="fill") if obj.image else ""
    image_preview.short_description = 'Предпросмотр'


class RealEstatePhoneNumberInline(admin.TabularInline):
    model = PhoneNumber
    extra = 1


@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ('floor', 'name',)
    search_fields = ('floor', 'name',)


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(ResidentialComplex)
class ResidentialComplexAdmin(admin.ModelAdmin):
    list_display = ('developer', 'name',)
    search_fields = ('developer', 'name',)


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(BuildingType)
class BuildingTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    list_display = ('year',)
    search_fields = ('year',)


@admin.register(ConditionType)
class ConditionTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(HeatingType)
class HeatingTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('district',)
    search_fields = ('district',)


@admin.register(ObjectType)
class ObjectTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(RoomLocation)
class RoomLocationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Telephone)
class TelephoneAdmin(admin.ModelAdmin):
    list_display = ('telephone',)
    search_fields = ('telephone',)


@admin.register(Internet)
class InternetAdmin(admin.ModelAdmin):
    list_display = ('internet',)
    search_fields = ('internet',)


@admin.register(BathRoom)
class BathRoomAdmin(admin.ModelAdmin):
    list_display = ('bathroom',)
    search_fields = ('bathroom',)


@admin.register(Gas)
class GasAdmin(admin.ModelAdmin):
    list_display = ('gas',)
    search_fields = ('gas',)


@admin.register(Balcony)
class BalconyAdmin(admin.ModelAdmin):
    list_display = ('balcony',)
    search_fields = ('balcony',)


@admin.register(MainDoor)
class MainDoorAdmin(admin.ModelAdmin):
    list_display = ('main_door',)
    search_fields = ('main_door',)


@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):
    list_display = ('parking',)
    search_fields = ('parking',)


@admin.register(Furniture)
class FurnitureAdmin(admin.ModelAdmin):
    list_display = ('furniture',)
    search_fields = ('furniture',)


@admin.register(FloorType)
class FloorTypeAdmin(admin.ModelAdmin):
    list_display = ('floor_type',)
    search_fields = ('floor_type',)


@admin.register(Safety)
class SafetyAdmin(admin.ModelAdmin):
    list_display = ('safety',)
    search_fields = ('safety',)


@admin.register(Other)
class OtherAdmin(admin.ModelAdmin):
    list_display = ('other',)
    search_fields = ('other',)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('document',)
    search_fields = ('document',)


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ('exchange_type',)
    search_fields = ('exchange_type',)
