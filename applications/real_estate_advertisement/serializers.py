from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample, extend_schema_field
from rest_framework import serializers
from .models import ApartmentAd, HouseAd, CommercialAd, RoomAd, DachaAd, PlotAd, ParkingAd
from ..common.serializers import SubscriptionSerializer, ExchangeSerializer
from ..real_estate.models import MarketingImage
from ..real_estate.serializers import RealEstateAdImageSerializer, PhoneNumberRealEstateSerializer, \
    ResidentialComplexSerializer, OtherSerializer, DocumentSerializer, SafetyRealEstateSerializer


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Real Estate Listing Example',
            value={
                "title": "Modern 2-Bedroom Apartments",
                "price": 325000.00,
                "currency": "USD",
                "city": "Bishkek",
                "images": [
                    {
                        "url": "https://example.com/images/villa1.jpg",
                    },
                    {
                        "url": "https://example.com/images/villa2.jpg",
                    }
                ],
            },
            response_only=True
        )
    ]
)
class BaseListRealEstateSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField(help_text="Цена в валюте")
    currency = serializers.CharField(source="currency.currency", read_only=True)
    city = serializers.CharField(source="city.city", read_only=True)
    title = serializers.CharField(read_only=True)
    images = RealEstateAdImageSerializer(
        many=True,
        source="images.all",
        help_text="URL-ы картинок ",
        read_only=True
    )

    @extend_schema_field(OpenApiTypes.STR)
    def get_price(self, obj):
        return f"{obj.price}{obj.currency}"

    class Meta:
        abstract = True
        fields = ["public_id", "price", "city", "title", "images"]


class ApartmentListRealEstate(BaseListRealEstateSerializer):
    class Meta(BaseListRealEstateSerializer.Meta):
        model = ApartmentAd


class HouseListRealEstate(BaseListRealEstateSerializer):
    class Meta(BaseListRealEstateSerializer.Meta):
        model = HouseAd


class CommercialListRealEstate(BaseListRealEstateSerializer):
    class Meta(BaseListRealEstateSerializer.Meta):
        model = CommercialAd


class RoomListRealEstate(BaseListRealEstateSerializer):
    class Meta(BaseListRealEstateSerializer.Meta):
        model = RoomAd


class DachaListRealEstate(BaseListRealEstateSerializer):
    class Meta(BaseListRealEstateSerializer.Meta):
        model = DachaAd


class PlotListRealEstate(BaseListRealEstateSerializer):
    class Meta(BaseListRealEstateSerializer.Meta):
        model = PlotAd


class ParkingListRealEstate(BaseListRealEstateSerializer):
    class Meta(BaseListRealEstateSerializer.Meta):
        model = ParkingAd


class PropertyCharacteristicsSerializer(serializers.Serializer):
    heating_type = serializers.SerializerMethodField()
    condition = serializers.SerializerMethodField()
    internet = serializers.SerializerMethodField()
    bathroom = serializers.SerializerMethodField()
    gas = serializers.SerializerMethodField()
    balcony = serializers.SerializerMethodField()
    main_door = serializers.SerializerMethodField()
    parking = serializers.SerializerMethodField()
    telephone = serializers.SerializerMethodField()
    furniture = serializers.SerializerMethodField()
    floor_type = serializers.SerializerMethodField()
    ceiling_height = serializers.FloatField()
    safety = SafetyRealEstateSerializer(
        many=True,
        help_text="Безопасность",
        read_only=True
    )
    other = OtherSerializer(
        many=True,
        read_only=True,
        help_text="Прочее"
    )
    document = DocumentSerializer(
        many=True,
        help_text="Документы",
        read_only=True
    )

    elevator = serializers.BooleanField()

    @extend_schema_field(OpenApiTypes.STR)
    def get_heating_type(self, obj):
        return getattr(obj.heating_type, 'name', None)

    @extend_schema_field(OpenApiTypes.STR)
    def get_condition(self, obj):
        return getattr(obj.condition, 'name', None)

    @extend_schema_field(OpenApiTypes.STR)
    def get_internet(self, obj):
        return getattr(obj.internet, 'internet', None)

    @extend_schema_field(OpenApiTypes.STR)
    def get_bathroom(self, obj):
        return getattr(obj.bathroom, 'bathroom', None)

    @extend_schema_field(OpenApiTypes.STR)
    def get_gas(self, obj):
        return getattr(obj.gas, 'gas', None)

    @extend_schema_field(OpenApiTypes.STR)
    def get_balcony(self, obj):
        return getattr(obj.balcony, 'balcony', None)

    @extend_schema_field(OpenApiTypes.STR)
    def get_main_door(self, obj):
        return getattr(obj.main_door, 'main_door', None)

    @extend_schema_field(OpenApiTypes.STR)
    def get_parking(self, obj):
        return getattr(obj.parking, 'parking', None)

    @extend_schema_field(OpenApiTypes.STR)
    def get_telephone(self, obj):
        return getattr(obj.telephone, 'telephone', None)

    @extend_schema_field(OpenApiTypes.STR)
    def get_furniture(self, obj):
        return getattr(obj.furniture, 'furniture', None)

    @extend_schema_field(OpenApiTypes.STR)
    def get_floor_type(self, obj):
        return getattr(obj.floor_type, 'floor_type', None)

    @extend_schema_field(OpenApiTypes.STR)
    def get_safety(self, obj):
        return getattr(obj.safety, 'safety', None)

    @extend_schema_field(OpenApiTypes.STR)
    def get_other(self, obj):
        return getattr(obj.other, 'other', None)


class LocationSerializer(serializers.Serializer):
    region = serializers.CharField(source="region.region")
    city = serializers.CharField(source="city.city")
    district = serializers.SerializerMethodField()
    address = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

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
    user = serializers.SerializerMethodField()
    ad_type = serializers.CharField()
    rent_period = serializers.CharField()
    price = serializers.SerializerMethodField(help_text="Цена в валюте")
    is_total_price = serializers.BooleanField()
    location = serializers.SerializerMethodField(
        help_text="Геоданные объекта"
    )
    property_characteristics = serializers.SerializerMethodField(
        help_text="Атрибуты недвижимости"
    )
    total_area = serializers.SerializerMethodField(
        help_text="В квадратных метрах: ",
    )
    subscription = SubscriptionSerializer()
    exchange = ExchangeSerializer()
    installment = serializers.BooleanField()
    mortgage = serializers.BooleanField()
    measurements_docs = serializers.SerializerMethodField()
    designing_docs = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField(
        help_text="URL-ы картинок ",
    )
    contact_number = PhoneNumberRealEstateSerializer(
        many=True,
        source="real_estate_phones.all",
        help_text="Контактный номер ",
        read_only=True
    )

    class Meta:
        abstract = True
        fields = [
            "public_id", "user", "ad_type", "rent_period", "title", "ENI_code", "description", "price", "is_total_price",
            "total_area", "location", "property_characteristics", "exchange", "installment", "mortgage", "measurements_docs",
            "designing_docs", "images", "link_Youtube", "created_at", "is_featured", "subscription", "view_count",
        ]

    @extend_schema_field(LocationSerializer)
    def get_location(self, obj):
        return LocationSerializer(obj).data

    @extend_schema_field(PropertyCharacteristicsSerializer)
    def get_property_characteristics(self, obj):
        return PropertyCharacteristicsSerializer(obj).data

    @extend_schema_field(OpenApiTypes.STR)
    def get_price(self, obj):
        return f"{obj.price}{obj.currency}"

    @extend_schema_field(OpenApiTypes.STR)
    def get_total_area(self, obj):
        return f"{obj.total_area} m2"

    @extend_schema_field(OpenApiTypes.STR)
    def get_user(self, obj):
        return f"{obj.user.email} - {obj.user.full_name}"

    @extend_schema_field(OpenApiTypes.STR)
    def get_measurements_docs(self, obj):
        request = self.context.get('request')
        if obj.measurements_docs and request:
            return request.build_absolute_uri(obj.measurements_docs.url)
        return None

    @extend_schema_field(OpenApiTypes.STR)
    def get_designing_docs(self, obj):
        request = self.context.get('request')
        if obj.designing_docs and request:
            return request.build_absolute_uri(obj.designing_docs.url)
        return None

    @extend_schema_field(serializers.ListSerializer(child=ImageSerializer()))
    def get_images(self, obj):
        request = self.context.get('request')
        images = []
        
        # Add real estate images
        for image in obj.images.all():
            if image.image and request:
                images.append({
                    'url': request.build_absolute_uri(image.image.url),
                    'is_main': image.is_main,
                    'type': 'property'
                })
        
        # Add marketing images for this property type
        marketing_images = MarketingImage.objects.filter(
            property_type=obj.property_type,
            is_active=True
        ).order_by('-created_at')
        
        for marketing_image in marketing_images:
            if marketing_image.image and request:
                images.append({
                    'url': request.build_absolute_uri(marketing_image.image.url),
                    'type': 'marketing',
                    'property_type': marketing_image.property_type
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
    construction_year = serializers.SerializerMethodField()
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

    class Meta(BaseRealEstateAdSerializer.Meta):
        model = ParkingAd
        fields = ["residential_complex"] + BaseRealEstateAdSerializer.Meta.fields
