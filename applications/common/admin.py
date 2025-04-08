from django.contrib import admin
from django.db.models import F, OrderBy
from .models import Region, City, Currency, Subscription, CountryName


@admin.register(CountryName)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('duration_days', 'price')
    search_fields = ('duration_days', 'price')


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('region',)
    search_fields = ('region',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by(OrderBy(F('ordering'), nulls_last=True), 'region')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('city',)
    search_fields = ('city',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by(OrderBy(F('ordering'), nulls_last=True), 'city')


admin.site.register(Currency)
