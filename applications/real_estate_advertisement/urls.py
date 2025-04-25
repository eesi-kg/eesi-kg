from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ApartmentAdViewSet, HouseAdViewSet, CommercialAdViewSet,
    RoomAdViewSet, PlotAdViewSet, DachaAdViewSet, ParkingAdViewSet,
    RealEstateAdViewSet
)

router = DefaultRouter()
router.register('apartments', ApartmentAdViewSet, basename='apartment')
router.register('houses', HouseAdViewSet, basename='house')
router.register('commercial', CommercialAdViewSet, basename='commercial')
router.register('rooms', RoomAdViewSet, basename='room')
router.register('plots', PlotAdViewSet, basename='plot')
router.register('dachas', DachaAdViewSet, basename='dacha')
router.register('parkings', ParkingAdViewSet, basename='parking')
router.register('', RealEstateAdViewSet, basename='main')

urlpatterns = [
    path('', include(router.urls)),
]
