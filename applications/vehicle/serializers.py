from rest_framework import serializers
from .models import (CommercialType, SpecialType, MotoType, Seria, OtherInfo, Fuel, Drive, Transmission, VehicleMake,
                     VehicleModel, VehicleYear, VehicleBodyType, VehicleGeneration, VehicleModification, VehicleColor,
                     Appearance, Salon, Media, Safety, Option, VehicleImage, PhoneNumber, VehicleModelDetail, Attribute,
                     VehicleModelImage)


class CommercialTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommercialType
        exclude = ("id", )


class SpecialTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialType
        exclude = ("id", )


class MotoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotoType
        exclude = ("id", )


class SeriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seria
        exclude = ("id", )


class OtherInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherInfo
        exclude = ("id", )


class FuelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fuel
        exclude = ("id", )


class DriveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drive
        exclude = ("id", )


class TransmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transmission
        exclude = ("id", )


class VehicleMakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleMake
        exclude = ("id", )


class VehicleYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleYear
        exclude = ("id", )


class VehicleBodyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleBodyType
        exclude = ("id", )


class VehicleGenerationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleGeneration
        exclude = ("id", )


class VehicleModificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleModification
        exclude = ("id", )


class VehicleColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleColor
        exclude = ("id", )


class AppearanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appearance
        exclude = ("id", )


class SalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salon
        exclude = ("id", )


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        exclude = ("id", )


class SafetySerializer(serializers.ModelSerializer):
    class Meta:
        model = Safety
        exclude = ("id", )


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        exclude = ("id", )


class VehicleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImage
        exclude = ("id", "vehicle")


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        exclude = ("id", 'ad')


class VehicleModelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleModelImage
        exclude = ("id",)


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ["name"]


class VehicleModelDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='attribute.name', read_only=True)
    value_string = serializers.CharField(read_only=True)

    class Meta:
        model = VehicleModelDetail
        fields = ['name', 'value_string']


class VehicleModelSerializer(serializers.ModelSerializer):
    images = VehicleModelImageSerializer(many=True, read_only=True)
    details = VehicleModelDetailSerializer(
        many=True,
        read_only=True,
        source='vehicle_model_detail'
    )

    def get_characteristics(self, obj):
        if obj.vehicle_model_detail.exists():
            return VehicleModelDetailSerializer(
                obj.vehicle_model_detail.all(),
                many=True
            ).data
        return None

    class Meta:
        model = VehicleModel
        fields = "__all__"
