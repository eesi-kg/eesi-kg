from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from .models import (Telephone, Internet, BathRoom, Gas, Balcony, MainDoor, Parking, Furniture,
                     FloorType, Safety, Other, Document, Developer, ResidentialComplex, Series, BuildingType,
                     HeatingType, ConditionType, RoomType, Year, Floor, ObjectType, RoomLocation, RealEstateAd,
                     PhoneNumber, RealEstateAdImage)


class TelephoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telephone
        exclude = ['id']


class InternetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internet
        exclude = ['id']


class BathRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = BathRoom
        exclude = ['id']


class GasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gas
        exclude = ['id']


class BalconySerializer(serializers.ModelSerializer):
    class Meta:
        model = Balcony
        exclude = ['id']


class MainDoorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainDoor
        exclude = ['id']


class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        exclude = ['id']


class FurnitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Furniture
        exclude = ['id']


class FloorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloorType
        exclude = ['id']


class SafetyRealEstateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Safety
        exclude = ['id']


class OtherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Other
        exclude = ['id']


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        exclude = ['id']


class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        exclude = ['id']


class ResidentialComplexSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResidentialComplex
        exclude = ['id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["developer"] = instance.developer.name
        return representation


class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        exclude = ['id']


class BuildingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingType
        exclude = ['id']


class HeatingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeatingType
        exclude = ['id']


class ConditionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConditionType
        exclude = ['id']


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        exclude = ['id']


class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        exclude = ['id']


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        exclude = ['id']


class ObjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectType
        exclude = ['id']


class RoomLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomLocation
        exclude = ['id']


class PhoneNumberRealEstateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        exclude = ['id', 'ad']


class RealEstateAdImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = RealEstateAdImage
        fields = ['image', ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
