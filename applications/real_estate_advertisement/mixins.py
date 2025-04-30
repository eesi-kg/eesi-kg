# from django.http import Http404
# from django_filters.rest_framework import DjangoFilterBackend
# from drf_spectacular.utils import extend_schema
# from rest_framework.filters import OrderingFilter, SearchFilter
# from rest_framework.pagination import PageNumberPagination
# from rest_framework.viewsets import ModelViewSet
# from rest_framework import filters, status
# from django.db.models import Prefetch, F
# from rest_framework.decorators import action
# from rest_framework.response import Response
#
# from .models import (
#     ApartmentAd, HouseAd, CommercialAd, RoomAd,
#     DachaAd, PlotAd, ParkingAd
# )
# from .serializers import (
#     ApartmentAdSerializer, HouseAdSerializer, CommercialAdSerializer,
#     RoomAdSerializer, DachaAdSerializer, PlotAdSerializer, ParkingAdSerializer,
# )
# from ..real_estate.models import RealEstateAdImage, RealEstateAd
#
# from .filters import (
#     ApartmentAdFilter, HouseAdFilter, CommercialAdFilter,
#     RoomAdFilter, DachaAdFilter, PlotAdFilter, ParkingAdFilter,
#     MainPageFilter
# )
#
#
# class RealEstatePageNumberPagination(PageNumberPagination):
#     page_size = 2
#     page_size_query_param = 'page_size'
#     max_page_size = 2
#     ordering = '-created_at'
#
#
# class ViewCountMixin:
#
#     def retrieve(self, request, *args, **kwargs):
#         response = super().retrieve(request, *args, **kwargs)
#         instance = RealEstateAd.objects.filter(pk=kwargs['pk'])
#         instance.update(view_count=F('view_count') + 1)
#
#         return response
#
#
# @extend_schema(tags=['Real Estate Advertisements'])
# class BaseRealEstateViewSet(ViewCountMixin, ModelViewSet):
#     http_method_names = ['get']
#     pagination_class = RealEstatePageNumberPagination
#     filter_backends = [
#         DjangoFilterBackend,
#         filters.SearchFilter,
#         filters.OrderingFilter
#     ]
#
#     serializer_class = None
#
#     def get_queryset(self):
#         queryset = super().get_queryset().filter(is_active=True)
#         if self.action == 'list':
#             queryset = self._optimize_detail_queryset(queryset)
#         elif self.action == 'retrieve':
#             queryset = self._optimize_detail_queryset(queryset)
#         return queryset
#
#     def _optimize_detail_queryset(self, queryset):
#         return queryset.select_related(
#             'city',
#             'realestatead_ptr__price',
#             'region',
#             'heating_type',
#             'condition',
#             'internet',
#             'bathroom',
#             'gas',
#             'balcony',
#             'main_door',
#             'parking',
#             'furniture',
#             'floor_type',
#         ).prefetch_related(
#             Prefetch('images',
#                      queryset=self.get_image_prefetch_queryset()),
#             'safety',
#             'other',
#             'document',
#             'telephone',
#         )
#
#     def get_image_prefetch_queryset(self):
#         return RealEstateAdImage.objects.only('id', 'ad', 'image')
#
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context['request'] = self.request
#         return context
#
#
# class ApartmentAdViewSet(BaseRealEstateViewSet):
#     queryset = ApartmentAd.objects.all()
#     serializer_class = ApartmentAdSerializer
#
#     filterset_class = ApartmentAdFilter
#
#     def _optimize_detail_queryset(self, queryset):
#         return super()._optimize_detail_queryset(queryset).select_related(
#             'rooms', 'residential_complex', 'series',
#             'building_type', 'construction_year',
#             'floor', 'max_floor'
#         )
#
#
# class HouseAdViewSet(BaseRealEstateViewSet):
#     queryset = HouseAd.objects.all()
#     serializer_class = HouseAdSerializer
#
#     filterset_class = HouseAdFilter
#
#     def _optimize_detail_queryset(self, queryset):
#         return super()._optimize_detail_queryset(queryset).select_related(
#             'rooms', 'building_type', 'floor'
#         )
#
#
# class CommercialAdViewSet(BaseRealEstateViewSet):
#     queryset = CommercialAd.objects.all()
#     serializer_class = CommercialAdSerializer
#
#     filterset_class = CommercialAdFilter
#
#     def _optimize_detail_queryset(self, queryset):
#         return super()._optimize_detail_queryset(queryset).select_related(
#             'object_type', 'residential_complex',
#             'building_type', 'construction_year',
#             'floor', 'max_floor'
#         )
#
#
# class RoomAdViewSet(BaseRealEstateViewSet):
#     queryset = RoomAd.objects.all()
#     serializer_class = RoomAdSerializer
#
#     filterset_class = RoomAdFilter
#
#     def _optimize_detail_queryset(self, queryset):
#         return super()._optimize_detail_queryset(queryset).select_related(
#             'rooms', 'room_location', 'floor', 'max_floor'
#         )
#
#
# class DachaAdViewSet(BaseRealEstateViewSet):
#     queryset = DachaAd.objects.all()
#     serializer_class = DachaAdSerializer
#
#     filterset_class = DachaAdFilter
#
#     def _optimize_detail_queryset(self, queryset):
#         return super()._optimize_detail_queryset(queryset).select_related(
#             'rooms', 'building_type'
#         )
#
#
# class PlotAdViewSet(BaseRealEstateViewSet):
#     queryset = PlotAd.objects.all()
#     serializer_class = PlotAdSerializer
#     filterset_class = PlotAdFilter
#
#
# class ParkingAdViewSet(BaseRealEstateViewSet):
#     queryset = ParkingAd.objects.all()
#     serializer_class = ParkingAdSerializer
#
#     filterset_class = ParkingAdFilter
#
#     def _optimize_detail_queryset(self, queryset):
#         return super()._optimize_detail_queryset(queryset).select_related(
#             'residential_complex'
#         )
#
#
# class BaseQuerysetOptimizer:
#     """
#     Base class for optimizing querysets with common patterns
#     """
#     @staticmethod
#     def optimize_base_queryset(queryset):
#         """
#         Base optimizations for all real estate advertisements
#         """
#         return queryset.select_related(
#             'city',
#             'region',
#             'realestatead_ptr__price',
#         ).prefetch_related(
#             Prefetch('images',
#                     queryset=RealEstateAdImage.objects.only('id', 'ad', 'image', 'is_main')
#                     .order_by('-is_main', 'id')),
#         )
#
#     @staticmethod
#     def optimize_apartment_queryset(queryset):
#         return queryset.select_related(
#             'rooms', 'residential_complex', 'series',
#             'building_type', 'construction_year',
#             'floor', 'max_floor'
#         )
#
#     @staticmethod
#     def optimize_house_queryset(queryset):
#         return queryset.select_related(
#             'rooms', 'building_type', 'floor'
#         )
#
#     @staticmethod
#     def optimize_commercial_queryset(queryset):
#         return queryset.select_related(
#             'object_type', 'residential_complex',
#             'building_type', 'construction_year',
#             'floor', 'max_floor'
#         )
#
#     @staticmethod
#     def optimize_room_queryset(queryset):
#         return queryset.select_related(
#             'rooms', 'room_location', 'floor', 'max_floor'
#         )
#
#     @staticmethod
#     def optimize_dacha_queryset(queryset):
#         return queryset.select_related(
#             'rooms', 'building_type'
#         )
#
#     @staticmethod
#     def optimize_parking_queryset(queryset):
#         return queryset.select_related(
#             'residential_complex'
#         )
#
#     @classmethod
#     def optimize_queryset(cls, queryset, model_class):
#         """
#         Apply all relevant optimizations based on model type
#         """
#         queryset = cls.optimize_base_queryset(queryset)
#
#         if model_class == ApartmentAd:
#             queryset = cls.optimize_apartment_queryset(queryset)
#         elif model_class == HouseAd:
#             queryset = cls.optimize_house_queryset(queryset)
#         elif model_class == CommercialAd:
#             queryset = cls.optimize_commercial_queryset(queryset)
#         elif model_class == RoomAd:
#             queryset = cls.optimize_room_queryset(queryset)
#         elif model_class == DachaAd:
#             queryset = cls.optimize_dacha_queryset(queryset)
#         elif model_class == ParkingAd:
#             queryset = cls.optimize_parking_queryset(queryset)
#
#         return queryset
#
#
# class RealEstateAdViewSet(BaseRealEstateViewSet):
#     filter_backends = [DjangoFilterBackend, OrderingFilter]
#     filterset_class = MainPageFilter
#     list_serializer_class = None
#     detail_serializer_class = None
#     ordering_fields = ['approved_at', 'price']  # Поля для сортировки
#     ordering = '-approved_at'
#
#     # Cache model mappings to avoid recreating on each request
#     MODEL_MAPPINGS = {
#         'apartment': (ApartmentAd, ApartmentAdSerializer, ApartmentAdFilter),
#         'house': (HouseAd, HouseAdSerializer, HouseAdFilter),
#         'commercial': (CommercialAd, CommercialAdSerializer, CommercialAdFilter),
#         'room': (RoomAd, RoomAdSerializer, RoomAdFilter),
#         'plot': (PlotAd, PlotAdSerializer, PlotAdFilter),
#         'dacha': (DachaAd, DachaAdSerializer, DachaAdFilter),
#         'parking': (ParkingAd, ParkingAdSerializer, ParkingAdFilter),
#     }
#
#     def get_queryset(self):
#         return ApartmentAd.objects.none()
#
#     def list(self, request, *args, **kwargs):
#         property_type = request.query_params.get('property_type', None)
#         results = []
#
#         if property_type and property_type in self.MODEL_MAPPINGS:
#             model_class, serializer_class, _ = self.MODEL_MAPPINGS[property_type]
#             queryset = self.filter_queryset(model_class.objects.filter(is_active=True))
#             queryset = BaseQuerysetOptimizer.optimize_queryset(queryset, model_class)
#             page = self.paginate_queryset(queryset)
#             if page is not None:
#                 serializer = serializer_class(page, many=True, context={'request': request})
#                 return self.get_paginated_response(serializer.data)
#
#             serializer = serializer_class(queryset, many=True, context={'request': request})
#             results.extend(serializer.data)
#         else:
#             combined_queryset = []
#             for model_class, serializer_class, _ in self.MODEL_MAPPINGS.values():
#                 queryset = self.filter_queryset(model_class.objects.filter(is_active=True))
#                 queryset = BaseQuerysetOptimizer.optimize_queryset(queryset, model_class)
#                 combined_queryset += list(queryset)
#             combined_queryset.sort(key=lambda x: x.created_at, reverse=True)
#             page = self.paginate_queryset(combined_queryset)
#             if page is not None:
#                 serialized_data = []
#                 for item in page:
#                     for model_class, serializer_class, _ in self.MODEL_MAPPINGS.values():
#                         if isinstance(item, model_class):
#                             serializer = serializer_class(item, context={'request': request})
#                             serialized_data.append(serializer.data)
#                             break
#                 return self.get_paginated_response(serialized_data)
#         return Response(results)
#
#     @action(detail=False, methods=['get'])
#     def property_types(self, request):
#         property_types = [
#             {'id': 'apartment', 'name': 'Квартиры'},
#             {'id': 'house', 'name': 'Дома'},
#             {'id': 'commercial', 'name': 'Коммерческая недвижимость'},
#             {'id': 'room', 'name': 'Комнаты'},
#             {'id': 'plot', 'name': 'Земельные участки'},
#             {'id': 'dacha', 'name': 'Дачи'},
#             {'id': 'parking', 'name': 'Парковки'},
#         ]
#         return Response(property_types)
#
#     def get_object(self):
#         """Находит объект по pk во всех связанных моделях с оптимизацией запроса"""
#         pk = self.kwargs.get('pk')
#         for model_class, _, _ in self.MODEL_MAPPINGS.values():
#             queryset = model_class.objects.filter(pk=pk)
#             queryset = BaseQuerysetOptimizer.optimize_queryset(queryset, model_class)
#             try:
#                 return queryset.get()
#             except model_class.DoesNotExist:
#                 continue
#         raise Http404("Объявление не найдено")
#
#     def retrieve(self, request, *args, **kwargs):
#         """Детализация одного объявления"""
#         try:
#             instance = self.get_object()
#         except Http404:
#             return Response(
#                 {"detail": "Объявление не найдено"},
#                 status=status.HTTP_404_NOT_FOUND
#             )
#
#         # Определяем нужный сериализатор
#         for model_class, serializer_class, _ in self.MODEL_MAPPINGS.values():
#             if instance._meta.model == model_class:
#                 used_serializer = self.detail_serializer_class or serializer_class
#                 serializer = used_serializer(instance, context={'request': request})
#                 return Response(serializer.data)
#
#         return Response(
#             {"detail": "Ошибка определения типа объявления"},
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )