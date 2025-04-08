from django.urls import path, include
from rest_framework import routers

from .views import (ApartmentAdViewSet, HouseAdViewSet, CommercialAdViewSet, RoomAdViewSet, DachaAdViewSet,
                    PlotAdViewSet, ParkingAdViewSet)

router = routers.DefaultRouter()
router.register("apartments", ApartmentAdViewSet, basename="apartments")
router.register("houses", HouseAdViewSet, basename="houses")
router.register("commercials", CommercialAdViewSet, basename="commercials")
router.register("rooms", RoomAdViewSet, basename="rooms")
router.register("dachas", DachaAdViewSet, basename="dachas")
router.register("plots", PlotAdViewSet, basename="plots")
router.register("parkings", ParkingAdViewSet, basename="parkings")


urlpatterns = [
    path("", include(router.urls)),
]
urlpatterns += router.urls
