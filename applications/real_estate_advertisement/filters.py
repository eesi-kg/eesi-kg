import django_filters
from django_filters import rest_framework as filters

from applications.common.models import Region, City, District
from .models import (
    RealEstateAd, ApartmentAd, HouseAd, CommercialAd,
    RoomAd, DachaAd, PlotAd, ParkingAd, BuildingType, Series,
    ResidentialComplex, RoomType
)
from ..real_estate.models import ConditionType, Document, ObjectType


class PriceRangeFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = RealEstateAd
        fields = ['min_price', 'max_price']


class AreaFilter(django_filters.FilterSet):
    min_area = django_filters.NumberFilter(field_name='total_area', lookup_expr='gte')
    max_area = django_filters.NumberFilter(field_name='total_area', lookup_expr='lte')

    class Meta:
        model = RealEstateAd
        fields = ['min_area', 'max_area']


class BaseRealEstateFilter(filters.FilterSet):
    region = django_filters.ModelChoiceFilter(
        field_name='region',
        queryset=Region.objects.all()
    )
    city = django_filters.ModelChoiceFilter(
        field_name='city',
        queryset=City.objects.all()
    )
    district = django_filters.ModelChoiceFilter(
        field_name='district',
        queryset=District.objects.all()
    )
    condition = django_filters.ModelChoiceFilter(
        field_name='condition',
        queryset=ConditionType.objects.all()
    )
    documents = django_filters.ModelMultipleChoiceFilter(
        field_name='document',
        queryset=Document.objects.all()
    )
    ceiling_height = django_filters.RangeFilter()

    class Meta:
        model = RealEstateAd
        fields = [
            'region', 'city', 'district',
            'condition', 'ceiling_height', 'user'
        ]


class ApartmentAdFilter(BaseRealEstateFilter, PriceRangeFilter, AreaFilter):
    rooms = django_filters.ModelChoiceFilter(
        field_name='rooms',
        queryset=RoomType.objects.all()
    )
    seria = django_filters.ModelChoiceFilter(
        field_name='series',
        queryset=Series.objects.all()
    )
    building_type = django_filters.ModelChoiceFilter(
        field_name='building_type',
        queryset=BuildingType.objects.all()
    )
    residential_complex = django_filters.ModelChoiceFilter(
        field_name='residential_complex',
        queryset=ResidentialComplex.objects.all()
    )
    floor = django_filters.RangeFilter()
    max_floor = django_filters.RangeFilter()
    is_total_price = django_filters.BooleanFilter()

    class Meta(BaseRealEstateFilter.Meta):
        model = ApartmentAd
        fields = BaseRealEstateFilter.Meta.fields + [
            'seria', 'residential_complex', 'floor',
            'max_floor', 'is_total_price', 'rooms', 'building_type'
        ]


class HouseAdFilter(BaseRealEstateFilter, PriceRangeFilter, AreaFilter):
    rooms = django_filters.ModelChoiceFilter(
        field_name='rooms',
        queryset=RoomType.objects.all()
    )
    floor = django_filters.RangeFilter()
    total_area = django_filters.RangeFilter()
    building_type = django_filters.ModelChoiceFilter(
        field_name='building_type',
        queryset=BuildingType.objects.all()
    )

    class Meta(BaseRealEstateFilter.Meta):
        model = HouseAd
        fields = BaseRealEstateFilter.Meta.fields + [
            'floor', 'total_area', 'rooms', 'building_type'
        ]


class CommercialAdFilter(BaseRealEstateFilter, PriceRangeFilter, AreaFilter):
    object_type = django_filters.ModelChoiceFilter(
        queryset=ObjectType.objects.all()
    )
    floor = django_filters.RangeFilter()
    max_floor = django_filters.RangeFilter()
    building_type = django_filters.ModelChoiceFilter(
        field_name='building_type',
        queryset=BuildingType.objects.all()
    )

    class Meta(BaseRealEstateFilter.Meta):
        model = CommercialAd
        fields = BaseRealEstateFilter.Meta.fields + [
            'object_type', 'floor', 'max_floor', 'building_type'
        ]


class RoomAdFilter(BaseRealEstateFilter, PriceRangeFilter):
    rooms = django_filters.ModelChoiceFilter(
        field_name='rooms',
        queryset=RoomType.objects.all()
    )
    floor = django_filters.RangeFilter()
    max_floor = django_filters.RangeFilter()

    class Meta(BaseRealEstateFilter.Meta):
        model = RoomAd
        fields = BaseRealEstateFilter.Meta.fields + [
            'floor', 'max_floor', 'rooms'
        ]


class DachaAdFilter(BaseRealEstateFilter, PriceRangeFilter, AreaFilter):
    rooms = django_filters.ModelChoiceFilter(
        field_name='rooms',
        queryset=RoomType.objects.all()
    )
    building_type = django_filters.ModelChoiceFilter(
        field_name='building_type',
        queryset=BuildingType.objects.all()
    )
    total_area = django_filters.RangeFilter()

    class Meta(BaseRealEstateFilter.Meta):
        model = DachaAd
        fields = BaseRealEstateFilter.Meta.fields + ['total_area', 'rooms', 'building_type']


class PlotAdFilter(BaseRealEstateFilter, PriceRangeFilter):
    class Meta(BaseRealEstateFilter.Meta):
        model = PlotAd
        fields = BaseRealEstateFilter.Meta.fields


class ParkingAdFilter(PriceRangeFilter):
    residential_complex = django_filters.ModelChoiceFilter(
        queryset=ResidentialComplex.objects.all()
    )

    class Meta:
        model = ParkingAd
        fields = ['residential_complex']


class MainPageFilter(PriceRangeFilter):
    PROPERTY_TYPE_CHOICES = (
        ('apartment', 'Квартиры'),
        ('house', 'Дома'),
        ('commercial', 'Коммерческие'),
        ('room', 'Комнаты'),
        ('plot', 'Участки'),
        ('dacha', 'Дачи'),
        ('parking', 'Парковки/Гаражи'),
    )
    property_type = filters.ChoiceFilter(choices=PROPERTY_TYPE_CHOICES, method='filter_by_property_type')
    city = filters.NumberFilter(field_name='city__id')
    region = filters.NumberFilter(field_name='region__id')

    class Meta:
        model = None  # Will be set dynamically
        fields = ['property_type', 'city', 'region']

    def filter_by_property_type(self, queryset, name, value):
        model_mappings = {
            'apartment': (ApartmentAd, ApartmentAdFilter),
            'house': (HouseAd, HouseAdFilter),
            'commercial': (CommercialAd, CommercialAdFilter),
            'room': (RoomAd, RoomAdFilter),
            'plot': (PlotAd, PlotAdFilter),
            'dacha': (DachaAd, DachaAdFilter),
            'parking': (ParkingAd, ParkingAdFilter),
        }

        if value in model_mappings:
            model_class, filter_class = model_mappings[value]
            # Create a new queryset for the specific model
            model_queryset = model_class.objects.filter(is_active=True)

            # Apply model-specific filters
            model_filter = filter_class(self.request.query_params, queryset=model_queryset)
            return model_filter.qs

        return queryset.none()