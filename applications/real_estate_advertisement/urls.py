from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ApartmentAdViewSet, HouseAdViewSet, CommercialAdViewSet,
    RoomAdViewSet, DachaAdViewSet, PlotAdViewSet, ParkingAdViewSet,
    MainPageViewSet
)

router = DefaultRouter()
router.register(r'apartments', ApartmentAdViewSet)
router.register(r'houses', HouseAdViewSet)
router.register(r'commercials', CommercialAdViewSet)
router.register(r'rooms', RoomAdViewSet)
router.register(r'dachas', DachaAdViewSet)
router.register(r'plots', PlotAdViewSet)
router.register(r'parkings', ParkingAdViewSet)
router.register(r'main', MainPageViewSet, basename='main')

urlpatterns = [
    path('', include(router.urls)),
]
