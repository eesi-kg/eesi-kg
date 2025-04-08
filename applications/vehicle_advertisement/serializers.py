from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample, extend_schema_field
from rest_framework import serializers

from .models import PassengerCar, CommercialCar, SpecialCar, Moto
from ..common.serializers import SubscriptionSerializer, CurrencySerializer, ExchangeSerializer, CountryNameSerializer
from ..vehicle.serializers import VehicleBodyTypeSerializer, VehicleMakeSerializer, VehicleModelSerializer, \
    VehicleColorSerializer, OtherInfoSerializer, AppearanceSerializer, SalonSerializer, MediaSerializer, \
    SafetySerializer, OptionSerializer, VehicleGenerationSerializer, FuelSerializer, DriveSerializer, \
    TransmissionSerializer, VehicleModificationSerializer, CommercialTypeSerializer, SeriaSerializer, \
    VehicleImageSerializer, PhoneNumberSerializer


@extend_schema_serializer(
        examples=[
            OpenApiExample(
                'Vehicle Listing Example',
                value={
                    "city": "Bishkek",
                    "price": "25000",
                    "currency": "USD",
                    "images": [
                        {"url": "https://example.com/image1.jpg", "description": "Front view"},
                        {"url": "https://example.com/image2.jpg", "description": "Interior"}
                    ],
                    "year": "2020",
                    "make": "Toyota",
                    "model": "Camry"
                },
                response_only=True
            )
        ]
    )
class BaseListVehicleSerializer(serializers.ModelSerializer):
    city = serializers.CharField(source='city.city')
    price = serializers.SerializerMethodField()
    currency = serializers.CharField(source="currency.currency", read_only=True)
    images = VehicleImageSerializer(many=True, read_only=True, help_text="URL-ы картинок ",)
    year = serializers.CharField(source='year.year', read_only=True)
    make = serializers.CharField(source='make.name', read_only=True)
    model = serializers.CharField(source='model.name', read_only=True)

    class Meta:
        abstract = True
        fields = ["public_id", "city", "price", "images", "year", "make", "model"]

    @extend_schema_field(OpenApiTypes.STR)
    def get_price(self, obj):
        return f"{obj.price}{obj.currency}"


class PassengerListSerializer(BaseListVehicleSerializer):
    class Meta(BaseListVehicleSerializer.Meta):
        model = PassengerCar


class CommercialListSerializer(serializers.ModelSerializer):
    class Meta(BaseListVehicleSerializer.Meta):
        model = PassengerCar


class SpecialListSerializer(serializers.ModelSerializer):
    class Meta(BaseListVehicleSerializer.Meta):
        model = PassengerCar


class MotoListSerializer(serializers.ModelSerializer):
    class Meta(BaseListVehicleSerializer.Meta):
        model = PassengerCar


class BaseVehicleSerializer(serializers.ModelSerializer):
    public_id = serializers.UUIDField(read_only=True)
    region = serializers.CharField(source='region.region')
    city = serializers.CharField(source='city.city')
    year = serializers.CharField(source='year.year', read_only=True)
    subscription = SubscriptionSerializer(read_only=True)
    make = VehicleMakeSerializer(read_only=True)
    model = VehicleModelSerializer(read_only=True)
    color = VehicleColorSerializer(read_only=True)
    registration_country = CountryNameSerializer(read_only=True)
    other_info = OtherInfoSerializer(read_only=True)
    currency = CurrencySerializer(read_only=True)
    exchange = ExchangeSerializer(read_only=True)
    appearance = AppearanceSerializer(many=True, read_only=True)
    salon = SalonSerializer(many=True, read_only=True)
    media = MediaSerializer(many=True, read_only=True)
    safety = SafetySerializer(many=True, read_only=True)
    option = OptionSerializer(many=True, read_only=True)
    images = VehicleImageSerializer(many=True, read_only=True)
    contact_numbers = PhoneNumberSerializer(many=True, read_only=True, source='vehicle_phones')

    class Meta:
        abstract = True
        fields = ["public_id", "region", "city", "subscription", "make", "model", "year", "color",
                  "registration_country", "other_info", "currency", "exchange", "appearance", "salon",
                  "media", "safety", "option", "qr_code", "condition", "mileage", "description",
                  "availability_in_KG", "cleared_in_KG", "vin", "plate", "price", "installment_payment",
                  "is_featured", "view_count", "link_Youtube", "created_at", "updated_at", "is_active",
                  "category", "user", "images", "contact_numbers",
                  ]


class PassengerCarSerializer(BaseVehicleSerializer):
    title = serializers.CharField()
    body_type = VehicleBodyTypeSerializer()
    generation = VehicleGenerationSerializer()
    fuel_type = FuelSerializer()
    drive_type = DriveSerializer()
    transmission = TransmissionSerializer()
    modification = VehicleModificationSerializer()
    steering = serializers.StringRelatedField()

    class Meta(BaseVehicleSerializer.Meta):
        model = PassengerCar
        fields = BaseVehicleSerializer.Meta.fields + [
            "title",
            "body_type",
            "generation",
            "fuel_type",
            "drive_type",
            "transmission",
            "modification",
            "steering",
        ]


class CommercialCarSerializer(BaseVehicleSerializer):
    title = serializers.CharField()
    commercial_type = CommercialTypeSerializer()
    body_type = VehicleBodyTypeSerializer()
    generation = VehicleGenerationSerializer()
    fuel_type = FuelSerializer()
    drive_type = DriveSerializer()
    transmission = TransmissionSerializer()
    modification = VehicleModificationSerializer()
    steering = serializers.StringRelatedField()

    class Meta(BaseVehicleSerializer.Meta):
        model = CommercialCar
        fields = BaseVehicleSerializer.Meta.fields + [
            "title",
            "commercial_type",
            "body_type",
            "generation",
            "fuel_type",
            "drive_type",
            "transmission",
            "modification",
            "steering",
        ]


class SpecialCarSerializer(BaseVehicleSerializer):
    title = serializers.CharField()
    special_type = CommercialTypeSerializer()
    fuel_type = FuelSerializer()
    steering = serializers.StringRelatedField()

    class Meta(BaseVehicleSerializer.Meta):
        model = SpecialCar
        fields = BaseVehicleSerializer.Meta.fields + [
            "title",
            "special_type",
            "fuel_type",
            "steering",
        ]


class MotoSerializer(BaseVehicleSerializer):
    title = serializers.CharField()
    moto_type = CommercialTypeSerializer()
    seria = SeriaSerializer()
    modification = VehicleModificationSerializer()

    class Meta(BaseVehicleSerializer.Meta):
        model = Moto
        fields = BaseVehicleSerializer.Meta.fields + [
            "title",
            "moto_type",
            "seria",
            "modification",
        ]


