from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.paginator import Paginator
from django.db.models import Q, Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import (
    ApartmentAd, HouseAd, CommercialAd, RoomAd, 
    DachaAd, PlotAd, ParkingAd
)
from .serializers import (
    ApartmentAdSerializer, HouseAdSerializer, CommercialAdSerializer,
    RoomAdSerializer, DachaAdSerializer, PlotAdSerializer, ParkingAdSerializer
)
from .filters import (
    ApartmentAdFilter, HouseAdFilter, CommercialAdFilter,
    RoomAdFilter, DachaAdFilter, PlotAdFilter, ParkingAdFilter,
    MainPageFilter
)
from ..real_estate.models import RealEstateAd, MarketingImage

# class BaseRealEstateViewSet(viewsets.ModelViewSet):
#     http_method_names = ['get']
#     def perform_create(self, serializer):
#         return serializer.save(user=self.request.user)

#     def perform_update(self, serializer):
#         return serializer.save()


# class ApartmentAdViewSet(BaseRealEstateViewSet):
#     queryset = ApartmentAd.objects.filter(is_active=True)
#     serializer_class = ApartmentAdSerializer
#     filterset_class = ApartmentAdFilter
#     lookup_field = 'public_id'


# class HouseAdViewSet(BaseRealEstateViewSet):
#     queryset = HouseAd.objects.filter(is_active=True)
#     serializer_class = HouseAdSerializer
#     filterset_class = HouseAdFilter
#     lookup_field = 'public_id'


# class CommercialAdViewSet(BaseRealEstateViewSet):
#     queryset = CommercialAd.objects.filter(is_active=True)
#     serializer_class = CommercialAdSerializer
#     filterset_class = CommercialAdFilter
#     lookup_field = 'public_id'


# class RoomAdViewSet(BaseRealEstateViewSet):
#     queryset = RoomAd.objects.filter(is_active=True)
#     serializer_class = RoomAdSerializer
#     filterset_class = RoomAdFilter
#     lookup_field = 'public_id'


# class DachaAdViewSet(BaseRealEstateViewSet):
#     queryset = DachaAd.objects.filter(is_active=True)
#     serializer_class = DachaAdSerializer
#     filterset_class = DachaAdFilter
#     lookup_field = 'public_id'


# class PlotAdViewSet(BaseRealEstateViewSet):
#     queryset = PlotAd.objects.filter(is_active=True)
#     serializer_class = PlotAdSerializer
#     filterset_class = PlotAdFilter
#     lookup_field = 'public_id'


# class ParkingAdViewSet(BaseRealEstateViewSet):
#     queryset = ParkingAd.objects.filter(is_active=True)
#     serializer_class = ParkingAdSerializer
#     filterset_class = ParkingAdFilter
#     lookup_field = 'public_id'


# class MainPageViewSet(viewsets.ViewSet):
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = MainPageFilter

#     @extend_schema(
#         parameters=[
#             OpenApiParameter(
#                 name='search',
#                 type=str,
#                 description='Search in title, description, address, region, city, property type, rooms, and residential complex'
#             ),
#             OpenApiParameter(
#                 name='property_type',
#                 type=str,
#                 description='Type of property (apartments, houses, commercials, rooms, dachas, plots, parkings)'
#             ),
#             OpenApiParameter(
#                 name='region',
#                 type=str,
#                 description='Region name'
#             ),
#             OpenApiParameter(
#                 name='city',
#                 type=str,
#                 description='City name'
#             ),
#             OpenApiParameter(
#                 name='min_price',
#                 type=float,
#                 description='Minimum price'
#             ),
#             OpenApiParameter(
#                 name='max_price',
#                 type=float,
#                 description='Maximum price'
#             ),
#             OpenApiParameter(
#                 name='min_area',
#                 type=float,
#                 description='Minimum area'
#             ),
#             OpenApiParameter(
#                 name='max_area',
#                 type=float,
#                 description='Maximum area'
#             ),
#             OpenApiParameter(
#                 name='page',
#                 type=int,
#                 description='Page number',
#                 default=1
#             ),
#             OpenApiParameter(
#                 name='page_size',
#                 type=int,
#                 description='Number of items per page',
#                 default=20
#             ),
#         ],
#         responses={
#             200: {
#                 'type': 'object',
#                 'properties': {
#                     'results': {
#                         'type': 'array',
#                         'items': {
#                             'type': 'object',
#                             'properties': {
#                                 'type': {'type': 'string'},
#                                 'data': {'type': 'object'}
#                             }
#                         }
#                     },
#                     'pagination': {
#                         'type': 'object',
#                         'properties': {
#                             'count': {'type': 'integer'},
#                             'total_pages': {'type': 'integer'},
#                             'current_page': {'type': 'integer'},
#                             'has_next': {'type': 'boolean'},
#                             'has_previous': {'type': 'boolean'},
#                             'next_page': {'type': 'integer', 'nullable': True},
#                             'previous_page': {'type': 'integer', 'nullable': True}
#                         }
#                     }
#                 }
#             }
#         }
#     )
#     def list(self, request):
#         property_type = request.query_params.get('property_type')
#         search_query = request.query_params.get('search', '')
#         page = int(request.query_params.get('page', 1))
#         page_size = int(request.query_params.get('page_size', 20))

#         base_queryset = ApartmentAd.objects.filter(
#             is_active=True
#         ).select_related(
#             'user', 'region', 'city', 'district', 'subscription',
#             'exchange', 'telephone', 'heating_type', 'condition',
#             'internet', 'bathroom', 'gas', 'balcony', 'main_door',
#             'parking', 'furniture', 'floor_type', 'rooms',
#             'residential_complex'
#         ).prefetch_related(
#             'safety', 'other', 'document', 'images', 'real_estate_phones'
#         )

#         if search_query:
#             base_queryset = base_queryset.filter(
#                 Q(title__icontains=search_query) |
#                 Q(description__icontains=search_query) |
#                 Q(address__icontains=search_query) |
#                 Q(region__region__icontains=search_query) |
#                 Q(city__city__icontains=search_query) |
#                 Q(property_type__icontains=search_query) |
#                 Q(rooms__name__icontains=search_query) |
#                 Q(residential_complex__name__icontains=search_query)
#             )

#         filter_instance = MainPageFilter(request.query_params, queryset=base_queryset)
#         filtered_queryset = filter_instance.qs

#         latest_objects = filtered_queryset.order_by('-created_at')

#         paginator = Paginator(latest_objects, page_size)
#         page_obj = paginator.get_page(page)

#         serialized_objects = []
#         for obj in page_obj:
#             if isinstance(obj, ApartmentAd):
#                 serializer = ApartmentAdSerializer(obj, context={'request': request})
#             elif isinstance(obj, HouseAd):
#                 serializer = HouseAdSerializer(obj, context={'request': request})
#             elif isinstance(obj, CommercialAd):
#                 serializer = CommercialAdSerializer(obj, context={'request': request})
#             elif isinstance(obj, RoomAd):
#                 serializer = RoomAdSerializer(obj, context={'request': request})
#             elif isinstance(obj, DachaAd):
#                 serializer = DachaAdSerializer(obj, context={'request': request})
#             elif isinstance(obj, PlotAd):
#                 serializer = PlotAdSerializer(obj, context={'request': request})
#             elif isinstance(obj, ParkingAd):
#                 serializer = ParkingAdSerializer(obj, context={'request': request})
            
#             serialized_objects.append({
#                 'type': obj.property_type,
#                 'data': serializer.data
#             })

#         pagination_info = {
#             'count': paginator.count,
#             'total_pages': paginator.num_pages,
#             'current_page': page,
#             'has_next': page_obj.has_next(),
#             'has_previous': page_obj.has_previous(),
#             'next_page': page + 1 if page_obj.has_next() else None,
#             'previous_page': page - 1 if page_obj.has_previous() else None
#         }

#         return Response({
#             'results': serialized_objects,
#             'pagination': pagination_info
#         })


from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.db.models import Q, Count, Case, When, BooleanField
from django.utils import timezone
from datetime import timedelta
from .models import ApartmentAd, HouseAd, CommercialAd, RoomAd, DachaAd, PlotAd, ParkingAd
from .serializers import (
    ApartmentAdSerializer, HouseAdSerializer, CommercialAdSerializer,
    RoomAdSerializer, DachaAdSerializer, PlotAdSerializer, ParkingAdSerializer
)
from .filters import (
    ApartmentAdFilter, HouseAdFilter, CommercialAdFilter,
    RoomAdFilter, DachaAdFilter, PlotAdFilter, ParkingAdFilter,
    MainPageFilter
)
import logging

logger = logging.getLogger(__name__)


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class BaseRealEstateViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return self.queryset.select_related(
            'region', 'city', 'district', 'subscription', 'telephone',
            'heating_type', 'condition', 'internet', 'bathroom', 'gas',
            'balcony', 'main_door', 'parking', 'furniture', 'floor_type', 'exchange'
        ).prefetch_related(
            'safety', 'other', 'document', 'real_estate_phones', 'images',
        ).annotate(
            image_count=Count('images'),
            has_main_image=Case(
                When(images__is_main=True, then=True),
                default=False,
                output_field=BooleanField()
            )
        )

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        return serializer.save()


class ApartmentAdViewSet(BaseRealEstateViewSet):
    queryset = ApartmentAd.objects.filter(is_active=True)\
        .select_related(
            'user', 'region', 'city', 'district', 'subscription', 'exchange', 'telephone',
            'heating_type', 'condition', 'internet', 'bathroom', 'gas', 'balcony', 'main_door',
            'parking', 'furniture', 'floor_type', 'rooms', 'residential_complex', 'series',
            'building_type', 'construction_year', 'floor', 'max_floor'
        )\
        .prefetch_related(
            'safety', 'other', 'document', 'images', 'real_estate_phones'
        )
    serializer_class = ApartmentAdSerializer
    filterset_class = ApartmentAdFilter
    lookup_field = 'public_id'


class HouseAdViewSet(BaseRealEstateViewSet):
    queryset = HouseAd.objects.filter(is_active=True)\
        .select_related(
            'user', 'region', 'city', 'district', 'subscription', 'exchange', 'telephone',
            'heating_type', 'condition', 'internet', 'bathroom', 'gas', 'balcony', 'main_door',
            'parking', 'furniture', 'floor_type', 'rooms', 'building_type', 'floor'
        )\
        .prefetch_related(
            'safety', 'other', 'document', 'images', 'real_estate_phones'
        )
    serializer_class = HouseAdSerializer
    filterset_class = HouseAdFilter
    lookup_field = 'public_id'


class CommercialAdViewSet(BaseRealEstateViewSet):
    queryset = CommercialAd.objects.filter(is_active=True)\
        .select_related(
            'user', 'region', 'city', 'district', 'subscription', 'exchange', 'telephone',
            'heating_type', 'condition', 'internet', 'bathroom', 'gas', 'balcony', 'main_door',
            'parking', 'furniture', 'floor_type', 'object_type', 'residential_complex', 'building_type',
            'construction_year', 'floor', 'max_floor'
        )\
        .prefetch_related(
            'safety', 'other', 'document', 'images', 'real_estate_phones'
        )
    serializer_class = CommercialAdSerializer
    filterset_class = CommercialAdFilter
    lookup_field = 'public_id'


class RoomAdViewSet(BaseRealEstateViewSet):
    queryset = RoomAd.objects.filter(is_active=True)\
        .select_related(
            'user', 'region', 'city', 'district', 'subscription', 'exchange', 'telephone',
            'heating_type', 'condition', 'internet', 'bathroom', 'gas', 'balcony', 'main_door',
            'parking', 'furniture', 'floor_type', 'rooms', 'room_location', 'floor', 'max_floor'
        )\
        .prefetch_related(
            'safety', 'other', 'document', 'images', 'real_estate_phones'
        )
    serializer_class = RoomAdSerializer
    filterset_class = RoomAdFilter
    lookup_field = 'public_id'


class DachaAdViewSet(BaseRealEstateViewSet):
    queryset = DachaAd.objects.filter(is_active=True)\
        .select_related(
            'user', 'region', 'city', 'district', 'subscription', 'exchange', 'telephone',
            'heating_type', 'condition', 'internet', 'bathroom', 'gas', 'balcony', 'main_door',
            'parking', 'furniture', 'floor_type', 'rooms', 'building_type', 'floor'
        )\
        .prefetch_related(
            'safety', 'other', 'document', 'images', 'real_estate_phones'
        )
    serializer_class = DachaAdSerializer
    filterset_class = DachaAdFilter
    lookup_field = 'public_id'


class PlotAdViewSet(BaseRealEstateViewSet):
    queryset = PlotAd.objects.filter(is_active=True)\
        .select_related(
            'user', 'region', 'city', 'district', 'subscription', 'exchange', 'telephone',
            'heating_type', 'condition', 'internet', 'bathroom', 'gas', 'balcony', 'main_door',
            'parking', 'furniture', 'floor_type'
        )\
        .prefetch_related(
            'safety', 'other', 'document', 'images', 'real_estate_phones'
        )
    serializer_class = PlotAdSerializer
    filterset_class = PlotAdFilter
    lookup_field = 'public_id'


class ParkingAdViewSet(BaseRealEstateViewSet):
    queryset = ParkingAd.objects.filter(is_active=True)\
        .select_related(
            'user', 'region', 'city', 'district', 'subscription', 'exchange', 'telephone',
            'heating_type', 'condition', 'internet', 'bathroom', 'gas', 'balcony', 'main_door',
            'parking', 'furniture', 'floor_type', 'residential_complex'
        )\
        .prefetch_related(
            'safety', 'other', 'document', 'images', 'real_estate_phones'
        )
    serializer_class = ParkingAdSerializer
    filterset_class = ParkingAdFilter
    lookup_field = 'public_id'


class MainPageViewSet(viewsets.ViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = MainPageFilter
    pagination_class = StandardPagination

    def get_querysets(self):
        property_type = self.request.query_params.get('property_type')
        search_query = self.request.query_params.get('search', '')

        # Ограничиваем выборку по времени (последние 30 дней)
        date_limit = timezone.now() - timedelta(days=30)

        # Определяем модели, их связи и property_type
        models = [
            (ApartmentAd, ['rooms', 'residential_complex', 'series', 'building_type', 'construction_year', 'floor', 'max_floor'], 'apartments'),
            (HouseAd, ['rooms', 'building_type', 'floor'], 'houses'),
            (CommercialAd, ['object_type', 'residential_complex', 'building_type', 'construction_year', 'floor', 'max_floor'], 'commercials'),
            (RoomAd, ['rooms', 'room_location', 'floor', 'max_floor'], 'rooms'),
            (DachaAd, ['rooms', 'building_type'], 'dachas'),
            (PlotAd, [], 'plots'),
            (ParkingAd, ['residential_complex'], 'parkings'),
        ]

        querysets = []
        for model, extra_selects, prop_type in models:
            if property_type and prop_type != property_type:
                continue

            qs = model.objects.filter(
                is_active=True,
                created_at__gte=date_limit
            ).select_related(
                'region', 'city', 'district', 'subscription', 'telephone',
                'heating_type', 'condition', 'internet', 'bathroom', 'gas',
                'balcony', 'main_door', 'parking', 'furniture', 'floor_type', 'exchange',
                *extra_selects
            ).prefetch_related(
                'safety', 'other', 'document', 'real_estate_phones', 'images',
            ).annotate(
                image_count=Count('images'),
                has_main_image=Case(
                    When(images__is_main=True, then=True),
                    default=False,
                    output_field=BooleanField()
                )
            )

            if search_query:
                qs = qs.filter(
                    Q(title__icontains=search_query) |
                    Q(description__icontains=search_query) |
                    Q(address__icontains=search_query) |
                    Q(region__region__icontains=search_query) |
                    Q(city__city__icontains=search_query) |
                    (Q(rooms__name__icontains=search_query) if 'rooms' in extra_selects else Q()) |
                    (Q(residential_complex__name__icontains=search_query) if 'residential_complex' in extra_selects else Q())
                )

            querysets.append((qs, prop_type))

        # Получаем последние объекты
        all_objects = []
        limit_per_model = 20  # Ограничиваем до 20 объектов на модель
        for qs, prop_type in querysets:
            objects = list(qs.order_by('-created_at')[:limit_per_model])
            logger.debug(f"Fetched {len(objects)} objects for {prop_type}")
            for obj in objects:
                all_objects.append((obj, prop_type))

        # Сортируем по created_at
        all_objects.sort(key=lambda x: x[0].created_at, reverse=True)
        logger.debug(f"Total objects after sorting: {len(all_objects)}")

        return all_objects[:100]  # Ограничиваем общий список до 100

    @extend_schema(
        parameters=[
            OpenApiParameter(name='search', type=str, description='Search in title, description, address, region, city, rooms, and residential complex'),
            OpenApiParameter(name='property_type', type=str, description='Type of property (apartments, houses, commercials, rooms, dachas, plots, parkings)'),
            OpenApiParameter(name='region', type=str, description='Region name'),
            OpenApiParameter(name='city', type=str, description='City name'),
            OpenApiParameter(name='min_price', type=float, description='Minimum price'),
            OpenApiParameter(name='max_price', type=float, description='Maximum price'),
            OpenApiParameter(name='min_area', type=float, description='Minimum area'),
            OpenApiParameter(name='max_area', type=float, description='Maximum area'),
            OpenApiParameter(name='page', type=int, description='Page number', default=1),
            OpenApiParameter(name='page_size', type=int, description='Number of items per page', default=20),
        ],
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'results': {'type': 'array', 'items': {'type': 'object'}},
                    'count': {'type': 'integer'},
                    'next': {'type': 'string', 'nullable': True},
                    'previous': {'type': 'string', 'nullable': True}
                }
            }
        }
    )
    def list(self, request):
        all_objects = self.get_querysets()

        # Ручная фильтрация
        filter_instance = self.filterset_class(request.query_params, queryset=ApartmentAd.objects.none())
        filter_params = filter_instance.data

        filtered_objects = []
        for obj, prop_type in all_objects:
            if filter_params.get('min_price') and obj.price < float(filter_params['min_price']):
                continue
            if filter_params.get('max_price') and obj.price > float(filter_params['max_price']):
                continue
            if filter_params.get('min_area') and obj.total_area and obj.total_area < float(filter_params['min_area']):
                continue
            if filter_params.get('max_area') and obj.total_area and obj.total_area > float(filter_params['max_area']):
                continue
            if filter_params.get('region') and obj.region and obj.region.region != filter_params['region']:
                continue
            if filter_params.get('city') and obj.city and obj.city.city != filter_params['city']:
                continue
            filtered_objects.append((obj, prop_type))

        logger.debug(f"Objects after filtering: {len(filtered_objects)}")

        paginator = self.pagination_class()
        page_number = request.query_params.get('page', 1)
        page_size = int(request.query_params.get('page_size', paginator.page_size))
        start = (int(page_number) - 1) * page_size
        end = start + page_size
        paginated_objects = filtered_objects[start:end]

        # Сериализация
        serialized_objects = []
        for obj, prop_type in paginated_objects:
            serializer_class = {
                'apartments': ApartmentAdSerializer,
                'houses': HouseAdSerializer,
                'commercials': CommercialAdSerializer,
                'rooms': RoomAdSerializer,
                'dachas': DachaAdSerializer,
                'plots': PlotAdSerializer,
                'parkings': ParkingAdSerializer
            }.get(prop_type, ApartmentAdSerializer)
            serializer = serializer_class(obj, context={'request': request})
            serialized_objects.append({
                'type': prop_type,
                'data': serializer.data
            })

        # Формируем ответ
        response_data = {
            'results': serialized_objects,
            'count': len(filtered_objects),
            'next': f"?page={int(page_number) + 1}&page_size={page_size}" if end < len(filtered_objects) else None,
            'previous': f"?page={int(page_number) - 1}&page_size={page_size}" if start > 0 else None
        }
        logger.debug(f"Paginated response: {len(serialized_objects)} objects on page {page_number}")
        return Response(response_data)