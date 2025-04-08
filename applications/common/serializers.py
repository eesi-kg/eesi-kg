from rest_framework import serializers
from .models import Region, City, District, Currency, Exchange, Subscription, CountryName


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["duration_days"]


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ["region"]


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["region", "city"]


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ["city", "district"]


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ["currency"]


class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = ["exchange_type"]


class CountryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryName
        exclude = ["id",]
