from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.pagination import CursorPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from django.db.models import Prefetch, F

from .models import (
    ApartmentAd, HouseAd, CommercialAd, RoomAd,
    DachaAd, PlotAd, ParkingAd
)
from .serializers import (
    ApartmentAdSerializer, HouseAdSerializer, CommercialAdSerializer,
    RoomAdSerializer, DachaAdSerializer, PlotAdSerializer, ParkingAdSerializer,
    ApartmentListRealEstate, HouseListRealEstate, CommercialListRealEstate,
    RoomListRealEstate, DachaListRealEstate, PlotListRealEstate, ParkingListRealEstate
)
from ..real_estate.models import RealEstateAdImage, RealEstateAd

from .filters import (
    ApartmentAdFilter, HouseAdFilter, CommercialAdFilter,
    RoomAdFilter, DachaAdFilter, PlotAdFilter, ParkingAdFilter
)


class RealEstateCursorPagination(CursorPagination):
    page_size = 20
    ordering = '-created_at'


class ViewCountMixin:

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        instance = RealEstateAd.objects.filter(pk=kwargs['pk'])
        instance.update(view_count=F('view_count') + 1)

        return response


@extend_schema(tags=['Real Estate Advertisements'])
class BaseRealEstateViewSet(ViewCountMixin, ModelViewSet):
    http_method_names = ['get']
    pagination_class = RealEstateCursorPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    list_serializer_class = None
    detail_serializer_class = None

    def get_serializer_class(self):
        return self.list_serializer_class if self.action == 'list' else self.detail_serializer_class

    def get_queryset(self):
        queryset = super().get_queryset().filter(realestatead_ptr__is_active=True)
        if self.action == 'list':
            queryset = self._optimize_list_queryset(queryset)
        elif self.action == 'retrieve':
            queryset = self._optimize_detail_queryset(queryset)
        return queryset

    def _optimize_list_queryset(self, queryset):
        return queryset.select_related(
            'city',
            'realestatead_ptr__price',
            'region',
        ).prefetch_related(
            Prefetch('images',
                     queryset=self.get_image_prefetch_queryset()),
        )

    def _optimize_detail_queryset(self, queryset):
        return queryset.select_related(
            'city',
            'realestatead_ptr__price',
            'region',
            'heating_type',
            'condition',
            'internet',
            'bathroom',
            'gas',
            'balcony',
            'main_door',
            'parking',
            'furniture',
            'floor_type',
        ).prefetch_related(
            Prefetch('images',
                     queryset=self.get_image_prefetch_queryset()),
            'safety',
            'other',
            'document',
            'telephone',
        )

    def get_image_prefetch_queryset(self):
        return RealEstateAdImage.objects.only('id', 'ad', 'image')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class ApartmentAdViewSet(BaseRealEstateViewSet):
    queryset = ApartmentAd.objects.all()
    list_serializer_class = ApartmentListRealEstate
    detail_serializer_class = ApartmentAdSerializer

    filterset_class = ApartmentAdFilter

    def _optimize_list_queryset(self, queryset):
        return super()._optimize_list_queryset(queryset)

    def _optimize_detail_queryset(self, queryset):
        return super()._optimize_detail_queryset(queryset).select_related(
            'rooms', 'residential_complex', 'series',
            'building_type', 'construction_year',
            'floor', 'max_floor'
        )


class HouseAdViewSet(BaseRealEstateViewSet):
    queryset = HouseAd.objects.all()
    list_serializer_class = HouseListRealEstate
    detail_serializer_class = HouseAdSerializer

    filterset_class = HouseAdFilter

    def _optimize_list_queryset(self, queryset):
        return super()._optimize_list_queryset(queryset).select_related(
            'rooms', 'building_type', 'floor'
        )

    def _optimize_detail_queryset(self, queryset):
        return super()._optimize_detail_queryset(queryset).select_related(
            'rooms', 'building_type', 'floor'
        )


class CommercialAdViewSet(BaseRealEstateViewSet):
    queryset = CommercialAd.objects.all()
    list_serializer_class = CommercialListRealEstate
    detail_serializer_class = CommercialAdSerializer

    filterset_class = CommercialAdFilter

    def _optimize_list_queryset(self, queryset):
        return super()._optimize_list_queryset(queryset).select_related(
            'object_type', 'residential_complex',
            'building_type', 'construction_year',
            'floor', 'max_floor'
        )

    def _optimize_detail_queryset(self, queryset):
        return super()._optimize_detail_queryset(queryset).select_related(
            'object_type', 'residential_complex',
            'building_type', 'construction_year',
            'floor', 'max_floor'
        )


class RoomAdViewSet(BaseRealEstateViewSet):
    queryset = RoomAd.objects.all()
    list_serializer_class = RoomListRealEstate
    detail_serializer_class = RoomAdSerializer

    filterset_class = RoomAdFilter

    def _optimize_list_queryset(self, queryset):
        return super()._optimize_list_queryset(queryset).select_related(
            'rooms', 'room_location', 'floor', 'max_floor'
        )

    def _optimize_detail_queryset(self, queryset):
        return super()._optimize_detail_queryset(queryset).select_related(
            'rooms', 'room_location', 'floor', 'max_floor'
        )


class DachaAdViewSet(BaseRealEstateViewSet):
    queryset = DachaAd.objects.all()
    list_serializer_class = DachaListRealEstate
    detail_serializer_class = DachaAdSerializer

    filterset_class = DachaAdFilter

    def _optimize_list_queryset(self, queryset):
        return super()._optimize_list_queryset(queryset).select_related(
            'rooms', 'building_type'
        )

    def _optimize_detail_queryset(self, queryset):
        return super()._optimize_detail_queryset(queryset).select_related(
            'rooms', 'building_type'
        )


class PlotAdViewSet(BaseRealEstateViewSet):
    queryset = PlotAd.objects.all()
    list_serializer_class = PlotListRealEstate
    detail_serializer_class = PlotAdSerializer
    filterset_class = PlotAdFilter


class ParkingAdViewSet(BaseRealEstateViewSet):
    queryset = ParkingAd.objects.all()
    list_serializer_class = ParkingListRealEstate
    detail_serializer_class = ParkingAdSerializer

    filterset_class = ParkingAdFilter

    def _optimize_list_queryset(self, queryset):
        return super()._optimize_list_queryset(queryset).select_related(
            'residential_complex'
        )

    def _optimize_detail_queryset(self, queryset):
        return super()._optimize_detail_queryset(queryset).select_related(
            'residential_complex'
        )