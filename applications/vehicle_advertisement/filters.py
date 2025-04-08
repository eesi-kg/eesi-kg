import django_filters

from .models import PassengerCar, CommercialCar, SpecialCar, Moto, SteeringChoices
from ..common.models import Currency, Region, City
from ..vehicle.models import VehicleMake, VehicleModel, CommercialType, Fuel, VehicleAd, VehicleBodyType, \
    Transmission, Drive, SpecialType, MotoType


class BaseVehicleFilter(django_filters.FilterSet):
    make = django_filters.ModelChoiceFilter(
        queryset=VehicleMake.objects.all(),
        field_name='make__name',
        label='Марка'
    )
    model = django_filters.ModelChoiceFilter(
        queryset=VehicleModel.objects.all(),
        field_name='model__name',
        label='Модель',
        method='filter_model'
    )
    year = django_filters.RangeFilter(
        field_name='year__year',
        label='Год выпуска'
    )
    price = django_filters.RangeFilter(
        label='Цена'
    )
    min_mileage = django_filters.NumberFilter(
        field_name='mileage',
        lookup_expr='gte',
        label='Минимальный пробег'
    )
    max_mileage = django_filters.NumberFilter(
        field_name='mileage',
        lookup_expr='lte',
        label='Максимальный пробег'
    )
    currency = django_filters.ModelChoiceFilter(
        queryset=Currency.objects.all(),
        label='Валюта'
    )
    steering = django_filters.ChoiceFilter(
        choices=SteeringChoices.choices,
        label='Руль'
    )
    condition = django_filters.ChoiceFilter(
        choices=VehicleAd.CONDITION_CHOICES,
        label='Состояние'
    )
    region = django_filters.ModelChoiceFilter(
        queryset=Region.objects.all(),
        label='Регион'
    )
    city = django_filters.ModelChoiceFilter(
        queryset=City.objects.all(),
        label='Город'
    )
    order_by = django_filters.OrderingFilter(
        fields=(
            ('price', 'price'),
            ('year__year', 'year'),
            ('mileage', 'mileage'),
            ('created_at', 'created_at'),
            ('make__name', 'make'),
            ('model__name', 'model'),
        ),
        field_labels={
            'price': 'Цена',
            'year__year': 'Год',
            'mileage': 'Пробег',
            'created_at': 'Дата создания',
            'make__name': 'Марка',
            'model__name': 'Модель'
        }
    )

    class Meta:
        model = VehicleAd
        fields = []

    def filter_model(self, queryset, name, value):
        if self.data.get('make'):
            return queryset.filter(model=value)
        return queryset


class PassengerCarFilter(BaseVehicleFilter):
    body_type = django_filters.ModelChoiceFilter(
        queryset=VehicleBodyType.objects.all(),
        label='Тип кузова'
    )
    fuel_type = django_filters.ModelChoiceFilter(
        queryset=Fuel.objects.all(),
        label='Тип топлива'
    )
    transmission = django_filters.ModelChoiceFilter(
        queryset=Transmission.objects.all(),
        label='Коробка передач'
    )
    drive_type = django_filters.ModelChoiceFilter(
        queryset=Drive.objects.all(),
        label='Привод'
    )

    def filter_model(self, queryset, name, value):
        if self.data.get('make'):
            return queryset.filter(model=value)
        return queryset

    class Meta(BaseVehicleFilter.Meta):
        model = PassengerCar
        fields = BaseVehicleFilter.Meta.fields + [
            'body_type', 'transmission', 'drive_type', 'fuel_type'
        ]


class CommercialCarFilter(BaseVehicleFilter):
    commercial_type = django_filters.ModelChoiceFilter(
        field_name='commercial_type__name',
        queryset=CommercialType.objects.all(),
        label='CommercialType'
    )
    fuel_type = django_filters.ModelChoiceFilter(
        queryset=Fuel.objects.all(),
        label='Тип топлива'
    )

    class Meta(BaseVehicleFilter.Meta):
        model = CommercialCar
        fields = BaseVehicleFilter.Meta.fields + ['commercial_type', 'fuel_type']


class SpecialCarFilter(BaseVehicleFilter):
    special_type = django_filters.ModelChoiceFilter(
        field_name='special_type__name',
        queryset=SpecialType.objects.all(),
        label='SpecialType'
    )
    fuel_type = django_filters.ModelChoiceFilter(
        queryset=Fuel.objects.all(),
        label='Тип топлива'
    )

    class Meta(BaseVehicleFilter.Meta):
        model = SpecialCar
        fields = BaseVehicleFilter.Meta.fields + ['special_type', 'fuel_type']


class MotoFilter(BaseVehicleFilter):
    moto_type = django_filters.ModelChoiceFilter(
        field_name='moto_type__name',
        queryset=MotoType.objects.all(),
        label='MotoType'
    )

    class Meta(BaseVehicleFilter.Meta):
        model = Moto
        fields = BaseVehicleFilter.Meta.fields + ['moto_type', ]
