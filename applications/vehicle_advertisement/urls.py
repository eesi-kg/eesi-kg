from django.urls import path, include
from rest_framework import routers

from .views import PassengerCarViewSet, CommercialCarViewSet, SpecialCarViewSet, MotoViewSet

router = routers.DefaultRouter()
router.register("passenger", PassengerCarViewSet, basename="passenger")
router.register("commercial", CommercialCarViewSet, basename="commercial")
router.register("special", SpecialCarViewSet, basename="special")
router.register("moto", MotoViewSet, basename="moto")


urlpatterns = [
    path("", include(router.urls)),
]
urlpatterns += router.urls
