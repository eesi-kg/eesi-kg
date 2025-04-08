# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.pagination import CursorPagination
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.viewsets import ModelViewSet
# from rest_framework import filters
#
# from applications.vehicle_advertisement.filters import (PassengerCarFilter, CommercialCarFilter, SpecialCarFilter,
#                                                         MotoFilter)
# from applications.vehicle_advertisement.models import PassengerCar, CommercialCar, SpecialCar, Moto
# from applications.vehicle_advertisement.serializers import (PassengerCarSerializer, CommercialCarSerializer, \
#     SpecialCarSerializer, MotoSerializer, PassengerListSerializer, CommercialListSerializer, SpecialListSerializer,
#                                                             MotoListSerializer)
#
#
# class VehicleCursorPagination(CursorPagination):
#     page_size = 20
#     ordering = '-created_at'
#
#
# class PassengerCarViewSet(ModelViewSet):
#     pagination_class = VehicleCursorPagination
#     filter_backends = [
#         DjangoFilterBackend,
#         filters.SearchFilter,
#     ]
#     filterset_class = PassengerCarFilter
#     queryset = PassengerCar.objects.filter(is_active=True)
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#
#         if self.action == 'list':
#             queryset = queryset.select_related(
#                 'city', 'make', 'model', 'currency'
#             ).prefetch_related(
#                 'images'
#             )
#         elif self.action == 'retrieve':
#             queryset = queryset.select_related(
#                 'region', 'city', 'subscription', 'make', 'model', 'color',
#                 'registration_country', 'other_info', 'currency', 'exchange',
#                 'body_type', 'generation', 'fuel_type', 'drive_type',
#                 'transmission', 'modification'
#             ).prefetch_related(
#                 'appearance', 'salon', 'images', 'safety', 'option', "media"
#             )
#         return queryset
#
#     def get_serializer_class(self):
#         if self.action == 'list':
#             return VehicleListSerializer
#         if self.action == 'retrieve':
#             return PassengerCarSerializer
#         return PassengerCarSerializer
#
#
# class CommercialCarViewSet(ModelViewSet):
#     pagination_class = VehicleCursorPagination
#     filter_backends = [
#         DjangoFilterBackend,
#         filters.SearchFilter,
#     ]
#     filterset_class = CommercialCarFilter
#     queryset = CommercialCar.objects.select_related(
#         'region', 'city', 'subscription', 'make', 'model', 'color',
#         'registration_country', 'other_info', 'currency', 'exchange',
#         'commercial_type', 'body_type', 'generation', 'fuel_type',
#         'drive_type', 'transmission', 'modification',
#     ).prefetch_related(
#         'appearance', 'salon', 'media', 'safety', 'option'
#     )
#     serializer_class = CommercialCarSerializer
#
#     @method_decorator(cache_page(60 * 15))
#     def list(self, request, *args, **kwargs):
#         return super().list(request, *args, **kwargs)
#
#
# class SpecialCarViewSet(ModelViewSet):
#     pagination_class = VehicleCursorPagination
#     filter_backends = [
#         DjangoFilterBackend,
#         filters.SearchFilter,
#     ]
#     filterset_class = SpecialCarFilter
#     permission_classes = [IsAuthenticated, ]
#     queryset = SpecialCar.objects.select_related(
#         'region', 'city', 'subscription', 'make', 'model', 'color',
#         'registration_country', 'other_info', 'currency', 'exchange',
#         'special_type', 'fuel_type'
#     ).prefetch_related(
#         'appearance', 'salon', 'media', 'safety', 'option'
#     )
#     serializer_class = SpecialCarSerializer
#
#     @method_decorator(cache_page(60 * 15))
#     def list(self, request, *args, **kwargs):
#         return super().list(request, *args, **kwargs)
#
#
# class MotoViewSet(ModelViewSet):
#     pagination_class = VehicleCursorPagination
#     filter_backends = [
#         DjangoFilterBackend,
#         filters.SearchFilter,
#     ]
#     filterset_class = MotoFilter
#     queryset = Moto.objects.select_related(
#         'region', 'city', 'subscription', 'make', 'model', 'color',
#         'registration_country', 'other_info', 'currency', 'exchange',
#         'moto_type', 'seria', 'modification',
#     ).prefetch_related(
#         'appearance', 'salon', 'media', 'safety', 'option'
#     )
#     serializer_class = MotoSerializer
#
#     @method_decorator(cache_page(60 * 15))
#     def list(self, request, *args, **kwargs):
#         return super().list(request, *args, **kwargs)

##################################################################################################
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.pagination import CursorPagination
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.viewsets import ModelViewSet
# from rest_framework import filters
#
# from applications.vehicle_advertisement.filters import (
#     PassengerCarFilter, CommercialCarFilter,
#     SpecialCarFilter, MotoFilter
# )
# from applications.vehicle_advertisement.models import (
#     PassengerCar, CommercialCar, SpecialCar, Moto
# )
# from applications.vehicle_advertisement.serializers import (
#     PassengerCarSerializer, CommercialCarSerializer,
#     SpecialCarSerializer, MotoSerializer, PassengerListSerializer,
#     CommercialListSerializer, SpecialListSerializer,
#     MotoListSerializer
# )
#
#
# class VehicleCursorPagination(CursorPagination):
#     page_size = 20
#     ordering = '-created_at'
#
#
# class BaseVehicleViewSet(ModelViewSet):
#     pagination_class = VehicleCursorPagination
#     filter_backends = [
#         DjangoFilterBackend,
#         filters.SearchFilter,
#     ]
#
#     def get_optimized_list_queryset(self, queryset):
#         return queryset.select_related(
#             'city', 'make', 'model', 'currency'
#         )
#
#     def get_optimized_detail_queryset(self, queryset):
#         return queryset.select_related(
#             'region', 'city', 'subscription', 'make', 'model',
#             'registration_country', 'other_info', 'currency', 'exchange',
#             'color'
#         ).prefetch_related(
#             'images', 'appearance', 'salon', 'safety', 'option', 'media'
#         )
#
#
# class PassengerCarViewSet(BaseVehicleViewSet):
#     filterset_class = PassengerCarFilter
#     queryset = PassengerCar.objects.filter(is_active=True)
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#
#         if self.action == 'list':
#             return self.get_optimized_list_queryset(queryset)
#         elif self.action == 'retrieve':
#             return self.get_optimized_detail_queryset(queryset).select_related(
#                 'body_type', 'generation', 'fuel_type',
#                 'drive_type', 'transmission', 'modification'
#             )
#         return queryset
#
#     def get_serializer_class(self):
#         if self.action == 'list':
#             return PassengerListSerializer
#         return PassengerCarSerializer
#
#
# class CommercialCarViewSet(BaseVehicleViewSet):
#     filterset_class = CommercialCarFilter
#     queryset = CommercialCar.objects.filter(is_active=True)
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#
#         if self.action == 'list':
#             return self.get_optimized_list_queryset(queryset).select_related(
#                 'commercial_type'
#             )
#         elif self.action == 'retrieve':
#             return self.get_optimized_detail_queryset(queryset).select_related(
#                 'commercial_type', 'body_type', 'generation',
#                 'fuel_type', 'drive_type', 'transmission', 'modification'
#             )
#         return queryset
#
#     def get_serializer_class(self):
#         if self.action == 'list':
#             return CommercialListSerializer
#         return CommercialCarSerializer
#
#
# class SpecialCarViewSet(BaseVehicleViewSet):
#     filterset_class = SpecialCarFilter
#     permission_classes = [IsAuthenticated]
#     queryset = SpecialCar.objects.filter(is_active=True)
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#
#         if self.action == 'list':
#             return self.get_optimized_list_queryset(queryset).select_related(
#                 'special_type'
#             )
#         elif self.action == 'retrieve':
#             return self.get_optimized_detail_queryset(queryset).select_related(
#                 'special_type', 'fuel_type'
#             )
#         return queryset
#
#     def get_serializer_class(self):
#         if self.action == 'list':
#             return SpecialListSerializer
#         return SpecialCarSerializer
#
#
# class MotoViewSet(BaseVehicleViewSet):
#     filterset_class = MotoFilter
#     queryset = Moto.objects.filter(is_active=True)
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#
#         if self.action == 'list':
#             return self.get_optimized_list_queryset(queryset).select_related(
#                 'moto_type'
#             )
#         elif self.action == 'retrieve':
#             return self.get_optimized_detail_queryset(queryset).select_related(
#                 'moto_type', 'seria', 'modification'
#             )
#         return queryset
#
#     def get_serializer_class(self):
#         if self.action == 'list':
#             return MotoListSerializer
#         return MotoSerializer

#######################################################################################


from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from applications.vehicle_advertisement.filters import (
    PassengerCarFilter, CommercialCarFilter,
    SpecialCarFilter, MotoFilter
)
from applications.vehicle_advertisement.models import (
    PassengerCar, CommercialCar, SpecialCar, Moto
)
from applications.vehicle_advertisement.serializers import (
    PassengerCarSerializer, CommercialCarSerializer,
    SpecialCarSerializer, MotoSerializer, PassengerListSerializer,
    CommercialListSerializer, SpecialListSerializer,
    MotoListSerializer
)


class VehicleCursorPagination(CursorPagination):
    page_size = 20
    ordering = '-created_at'


@extend_schema(tags=['Vehicle Advertisements'])
class BaseVehicleViewSet(ModelViewSet):
    http_method_names = ['get']
    pagination_class = VehicleCursorPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    list_serializer_class = None
    detail_serializer_class = None
    list_select_related = ()
    retrieve_select_related = ()
    base_list_fields = [
        'price', 'year',
        'city_id', 'city__city',
        'make_id', 'make__name',
        'model_id', 'model__name',
        'currency_id', 'currency__currency'
    ]

    def get_serializer_class(self):
        return self.list_serializer_class if self.action == 'list' else self.detail_serializer_class

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == 'list':
            queryset = self.get_optimized_list_queryset(queryset)
            if self.list_select_related:
                queryset = queryset.select_related(*self.list_select_related)
        elif self.action == 'retrieve':
            queryset = self.get_optimized_detail_queryset(queryset)
            if self.retrieve_select_related:
                queryset = queryset.select_related(*self.retrieve_select_related)
        return queryset

    def get_optimized_list_queryset(self, queryset):
        return queryset.select_related(
            'city', 'make', 'model', 'currency', 'year'
        ).prefetch_related('images').all()

    def get_optimized_detail_queryset(self, queryset):
        return queryset.select_related(
            'region', 'city', 'subscription', 'make', 'model',
            'registration_country', 'other_info', 'currency', 'exchange',
            'color'
        ).prefetch_related(
            'images', 'appearance', 'salon', 'safety', 'option', 'media'
        )


class PassengerCarViewSet(BaseVehicleViewSet):
    filterset_class = PassengerCarFilter
    queryset = PassengerCar.objects.filter(is_active=True)
    list_serializer_class = PassengerListSerializer
    detail_serializer_class = PassengerCarSerializer
    retrieve_select_related = (
        'body_type', 'generation', 'fuel_type',
        'drive_type', 'transmission', 'modification'
    )


class CommercialCarViewSet(BaseVehicleViewSet):
    filterset_class = CommercialCarFilter
    queryset = CommercialCar.objects.filter(is_active=True)
    list_serializer_class = CommercialListSerializer
    detail_serializer_class = CommercialCarSerializer
    list_select_related = ('commercial_type',)
    retrieve_select_related = (
        'commercial_type', 'body_type', 'generation',
        'fuel_type', 'drive_type', 'transmission', 'modification'
    )
    base_list_fields = BaseVehicleViewSet.base_list_fields + ['commercial_type_id']


class SpecialCarViewSet(BaseVehicleViewSet):
    filterset_class = SpecialCarFilter
    permission_classes = [IsAuthenticated]
    queryset = SpecialCar.objects.filter(is_active=True)
    list_serializer_class = SpecialListSerializer
    detail_serializer_class = SpecialCarSerializer
    list_select_related = ('special_type',)
    retrieve_select_related = ('special_type', 'fuel_type')
    base_list_fields = BaseVehicleViewSet.base_list_fields + ['special_type_id']


class MotoViewSet(BaseVehicleViewSet):
    filterset_class = MotoFilter
    queryset = Moto.objects.filter(is_active=True)
    list_serializer_class = MotoListSerializer
    detail_serializer_class = MotoSerializer
    list_select_related = ('moto_type',)
    retrieve_select_related = ('moto_type', 'seria', 'modification')
    base_list_fields = BaseVehicleViewSet.base_list_fields + ['moto_type_id']