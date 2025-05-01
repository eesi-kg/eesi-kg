from django.core.exceptions import FieldDoesNotExist
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample, extend_schema_field
from rest_framework import serializers
from .models import ApartmentAd, HouseAd, CommercialAd, RoomAd, DachaAd, PlotAd, ParkingAd
from ..common.serializers import SubscriptionSerializer, ExchangeSerializer
from ..real_estate.models import MarketingImage, ConditionType
from ..real_estate.serializers import PhoneNumberRealEstateSerializer, \
    ResidentialComplexSerializer, OtherSerializer, DocumentSerializer, SafetyRealEstateSerializer


class PropertyCharacteristicsSerializer(serializers.Serializer):
    heating_type = serializers.CharField(source='heating_type.name', allow_null=True)
    condition = serializers.CharField(source='condition.name', allow_null=True)
    internet = serializers.CharField(source='internet.internet', allow_null=True)
    bathroom = serializers.CharField(source='bathroom.bathroom', allow_null=True)
    gas = serializers.CharField(source='gas.gas', allow_null=True)
    balcony = serializers.CharField(source='balcony.balcony', allow_null=True)
    main_door = serializers.CharField(source='main_door.main_door', allow_null=True)
    parking = serializers.CharField(source='parking.parking', allow_null=True)
    telephone = serializers.CharField(source='telephone.telephone', allow_null=True)
    furniture = serializers.CharField(source='furniture.furniture', allow_null=True)
    floor_type = serializers.CharField(source='floor_type.floor_type', allow_null=True)
    ceiling_height = serializers.FloatField(allow_null=True)
    safety = SafetyRealEstateSerializer(many=True, read_only=True)
    other = OtherSerializer(many=True, read_only=True)
    document = DocumentSerializer(many=True, read_only=True)
    elevator = serializers.BooleanField(allow_null=True)


class LocationSerializer(serializers.Serializer):
    region = serializers.CharField(source='region.region', allow_null=True)
    city = serializers.CharField(source='city.city', allow_null=True)
    district = serializers.CharField(source='district.district', allow_null=True)
    address = serializers.CharField(allow_null=True)
    latitude = serializers.FloatField(allow_null=True)
    longitude = serializers.FloatField(allow_null=True)

    @extend_schema_field(OpenApiTypes.STR)
    def get_district(self, obj):
        return getattr(obj.district, 'district', None)


class ImageSerializer(serializers.Serializer):
    url = serializers.URLField()
    type = serializers.CharField()
    is_main = serializers.BooleanField(required=False)
    property_type = serializers.CharField(required=False)


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Real Estate Ad Example',
            value={
                "public_id": "ad-12345",
                "title": "Luxury Villa in Bishkek",
                "description": "5-bedroom villa with private pool",
                "price": 2500000.00,
                "total_area": 450.5,
                "latitude": 74.2048,
                "longitude": 42.2708,
                "property_characteristics": {
                    "bedrooms": 5,
                    "bathrooms": 6,
                    "year_built": 2020
                },
                "currency": "USD",
                "exchange": "FIXED",
                "safety": [{"feature": "24/7 Security"}],
                "images": [{"url": "https://example.com/image1.jpg"}]
            },
            request_only=False,
            response_only=True
        )
    ]
)
class BaseRealEstateAdSerializer(serializers.ModelSerializer):
    def get_marketing_images(self, obj):
        return list(
            MarketingImage.objects.filter(
                is_active=True,
                property_type=obj.property_type
            ).order_by('-created_at').values('image')
        )

    public_id = serializers.CharField()
    user = serializers.CharField(source='user.email')
    ad_type = serializers.CharField()
    rent_period = serializers.CharField(allow_null=True)
    price = serializers.CharField(source='get_price_display')
    is_total_price = serializers.BooleanField()
    location = LocationSerializer(read_only=True)
    property_characteristics = PropertyCharacteristicsSerializer(read_only=True)
    total_area = serializers.CharField(source='get_total_area', allow_null=True)
    subscription = SubscriptionSerializer()
    exchange = ExchangeSerializer(allow_null=True)
    installment = serializers.BooleanField(allow_null=True)
    mortgage = serializers.BooleanField(allow_null=True)
    measurements_docs = serializers.URLField(source='get_measurements_docs_url', allow_null=True)
    designing_docs = serializers.URLField(source='get_designing_docs_url', allow_null=True)
    images = serializers.SerializerMethodField()
    contact_number = PhoneNumberRealEstateSerializer(source='real_estate_phones', many=True, read_only=True)
    image_count = serializers.IntegerField(read_only=True)
    has_main_image = serializers.BooleanField(read_only=True)

    class Meta:
        abstract = True
        fields = [
            'public_id', 'user', 'ad_type', 'rent_period', 'title', 'ENI_code', 'description',
            'price', 'is_total_price', 'total_area', 'location', 'property_characteristics',
            'exchange', 'installment', 'mortgage', 'measurements_docs', 'designing_docs',
            'images', 'link_Youtube', 'created_at', 'is_featured', 'subscription', 'view_count',
            'contact_number', 'image_count', 'has_main_image'
        ]

    def get_images(self, obj):
        request = self.context.get('request')
        images = []
        for image in obj.images.all():
            if image.image and request:
                images.append({
                    'url': request.build_absolute_uri(image.image.url),
                    'is_main': image.is_main,
                    'type': 'property'
                })
        for marketing_image in self.get_marketing_images(obj):
            if marketing_image['image'] and request:
                images.append({
                    'url': request.build_absolute_uri(marketing_image['image']),
                    'type': 'marketing',
                    'property_type': obj.property_type
                })
        return images


class ApartmentAdSerializer(BaseRealEstateAdSerializer):
    rooms = serializers.SerializerMethodField()
    residential_complex = ResidentialComplexSerializer()
    series = serializers.CharField(source="series.name")
    building_type = serializers.CharField(source="building_type.name")
    construction_year = serializers.SerializerMethodField()
    floor = serializers.CharField(source="floor.floor")
    max_floor = serializers.CharField(source="max_floor.floor")

    class Meta(BaseRealEstateAdSerializer.Meta):
        model = ApartmentAd
        fields = [
            "rooms", "residential_complex", "series",
            "building_type", "construction_year", "floor", "max_floor"
        ] + BaseRealEstateAdSerializer.Meta.fields

    @extend_schema_field(OpenApiTypes.STR)
    def get_construction_year(self, obj):
        return getattr(obj.construction_year, 'year', None)

    @extend_schema_field(OpenApiTypes.STR)
    def get_rooms(self, obj):
        return f"{obj.rooms.name}-{obj.rooms.room_count}"


class HouseAdSerializer(BaseRealEstateAdSerializer):
    rooms = serializers.SerializerMethodField()
    building_type = serializers.CharField(source="building_type.name")
    floor = serializers.CharField(source="floor.floor")
    area = serializers.SerializerMethodField(
        help_text="В квадратных метрах m2",
    )
    total_area = serializers.SerializerMethodField(
        help_text="В квадратных метрах m2",
    )

    class Meta(BaseRealEstateAdSerializer.Meta):
        model = HouseAd
        fields = [
            "rooms", "building_type", "floor", "area", "total_area"
        ] + BaseRealEstateAdSerializer.Meta.fields

    @extend_schema_field(OpenApiTypes.STR)
    def get_total_area(self, obj):
        return f"{obj.total_area} m2"

    @extend_schema_field(OpenApiTypes.STR)
    def get_area(self, obj):
        return f"{obj.area} m2"

    @extend_schema_field(OpenApiTypes.STR)
    def get_rooms(self, obj):
        return f"{obj.rooms.name}-{obj.rooms.room_count}"


class CommercialAdSerializer(BaseRealEstateAdSerializer):
    object_type = serializers.CharField(source="object_type.name")
    building_type = serializers.CharField(source="building_type.name")
    construction_year = serializers.SerializerMethodField()
    floor = serializers.CharField(source="floor.floor")
    max_floor = serializers.CharField(source="max_floor.floor")
    total_area = serializers.SerializerMethodField(
        help_text="В квадратных метрах m2",
    )

    class Meta(BaseRealEstateAdSerializer.Meta):
        model = CommercialAd
        fields = [
            "object_type", "building_type", "construction_year",
            "floor", "max_floor", "total_area"
        ] + BaseRealEstateAdSerializer.Meta.fields

    @extend_schema_field(OpenApiTypes.STR)
    def get_construction_year(self, obj):
        return getattr(obj.construction_year, 'year', None)

    @extend_schema_field(OpenApiTypes.STR)
    def get_total_area(self, obj):
        return f"{obj.total_area} m2"


class RoomAdSerializer(BaseRealEstateAdSerializer):
    rooms = serializers.SerializerMethodField()
    room_location = serializers.CharField(source="room_location.name")
    floor = serializers.CharField(source="floor.floor")
    max_floor = serializers.CharField(source="max_floor.floor")

    class Meta(BaseRealEstateAdSerializer.Meta):
        model = RoomAd
        fields = [
            "rooms", "room_location", "floor", "max_floor"
        ] + BaseRealEstateAdSerializer.Meta.fields

    @extend_schema_field(OpenApiTypes.STR)
    def get_rooms(self, obj):
        return f"{obj.rooms.name}-{obj.rooms.room_count}"


class PlotAdSerializer(BaseRealEstateAdSerializer):

    class Meta(BaseRealEstateAdSerializer.Meta):
        model = PlotAd


class DachaAdSerializer(BaseRealEstateAdSerializer):
    rooms = serializers.SerializerMethodField()
    building_type = serializers.CharField(source="building_type.name")
    construction_year = serializers.SerializerMethodField()
    floor = serializers.CharField(source="floor.floor")
    area = serializers.SerializerMethodField(
        help_text="В квадратных метрах m2",
    )
    total_area = serializers.SerializerMethodField(
        help_text="В квадратных метрах m2",
    )

    class Meta(BaseRealEstateAdSerializer.Meta):
        model = DachaAd
        fields = [
            "rooms", "building_type", "construction_year", "floor", "area", "total_area"
        ] + BaseRealEstateAdSerializer.Meta.fields

    @extend_schema_field(OpenApiTypes.STR)
    def get_construction_year(self, obj):
        return getattr(obj.construction_year, 'year', None)

    @extend_schema_field(OpenApiTypes.STR)
    def get_total_area(self, obj):
        return f"{obj.total_area} m2"

    @extend_schema_field(OpenApiTypes.STR)
    def get_area(self, obj):
        return f"{obj.area} m2"

    @extend_schema_field(OpenApiTypes.STR)
    def get_rooms(self, obj):
        return f"{obj.rooms.room_count}-{obj.rooms.name}"


class ParkingAdSerializer(BaseRealEstateAdSerializer):
    residential_complex = ResidentialComplexSerializer()

    @extend_schema_field(OpenApiTypes.STR)
    def get_total_area(self, obj):
        try:
            obj._meta.get_field("total_area")
            return f"{obj.total_area} m2"
        except FieldDoesNotExist:
            return None

    class Meta(BaseRealEstateAdSerializer.Meta):
        model = ParkingAd
        fields = [
                     field for field in BaseRealEstateAdSerializer.Meta.fields
                     if field not in ["total_area", "property_characteristics"]
                 ] + ["residential_complex"]
