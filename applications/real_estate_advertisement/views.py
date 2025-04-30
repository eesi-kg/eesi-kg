from rest_framework import viewsets
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.db.models import Q
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


class ApartmentAdViewSet(viewsets.ModelViewSet):
    queryset = ApartmentAd.objects.filter(is_active=True)
    serializer_class = ApartmentAdSerializer
    filterset_class = ApartmentAdFilter
    lookup_field = 'public_id'


class HouseAdViewSet(viewsets.ModelViewSet):
    queryset = HouseAd.objects.filter(is_active=True)
    serializer_class = HouseAdSerializer
    filterset_class = HouseAdFilter
    lookup_field = 'public_id'


class CommercialAdViewSet(viewsets.ModelViewSet):
    queryset = CommercialAd.objects.filter(is_active=True)
    serializer_class = CommercialAdSerializer
    filterset_class = CommercialAdFilter
    lookup_field = 'public_id'


class RoomAdViewSet(viewsets.ModelViewSet):
    queryset = RoomAd.objects.filter(is_active=True)
    serializer_class = RoomAdSerializer
    filterset_class = RoomAdFilter
    lookup_field = 'public_id'


class DachaAdViewSet(viewsets.ModelViewSet):
    queryset = DachaAd.objects.filter(is_active=True)
    serializer_class = DachaAdSerializer
    filterset_class = DachaAdFilter
    lookup_field = 'public_id'


class PlotAdViewSet(viewsets.ModelViewSet):
    queryset = PlotAd.objects.filter(is_active=True)
    serializer_class = PlotAdSerializer
    filterset_class = PlotAdFilter
    lookup_field = 'public_id'


class ParkingAdViewSet(viewsets.ModelViewSet):
    queryset = ParkingAd.objects.filter(is_active=True)
    serializer_class = ParkingAdSerializer
    filterset_class = ParkingAdFilter
    lookup_field = 'public_id'


class MainPageViewSet(viewsets.ViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = MainPageFilter

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='search',
                type=str,
                description='Search in title, description, address, region, city, property type, rooms, and residential complex'
            ),
            OpenApiParameter(
                name='property_type',
                type=str,
                description='Type of property (apartments, houses, commercials, rooms, dachas, plots, parkings)'
            ),
            OpenApiParameter(
                name='region',
                type=str,
                description='Region name'
            ),
            OpenApiParameter(
                name='city',
                type=str,
                description='City name'
            ),
            OpenApiParameter(
                name='min_price',
                type=float,
                description='Minimum price'
            ),
            OpenApiParameter(
                name='max_price',
                type=float,
                description='Maximum price'
            ),
            OpenApiParameter(
                name='min_area',
                type=float,
                description='Minimum area'
            ),
            OpenApiParameter(
                name='max_area',
                type=float,
                description='Maximum area'
            ),
            OpenApiParameter(
                name='page',
                type=int,
                description='Page number',
                default=1
            ),
            OpenApiParameter(
                name='page_size',
                type=int,
                description='Number of items per page',
                default=20
            ),
        ],
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'results': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'type': {'type': 'string'},
                                'data': {'type': 'object'}
                            }
                        }
                    },
                    'pagination': {
                        'type': 'object',
                        'properties': {
                            'count': {'type': 'integer'},
                            'total_pages': {'type': 'integer'},
                            'current_page': {'type': 'integer'},
                            'has_next': {'type': 'boolean'},
                            'has_previous': {'type': 'boolean'},
                            'next_page': {'type': 'integer', 'nullable': True},
                            'previous_page': {'type': 'integer', 'nullable': True}
                        }
                    }
                }
            }
        }
    )
    def list(self, request):
        property_type = request.query_params.get('property_type')
        search_query = request.query_params.get('search', '')
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))

        base_queryset = ApartmentAd.objects.filter(
            is_active=True
        ).select_related(
            'user', 'region', 'city', 'district', 'subscription',
            'exchange', 'telephone', 'heating_type', 'condition',
            'internet', 'bathroom', 'gas', 'balcony', 'main_door',
            'parking', 'furniture', 'floor_type', 'rooms',
            'residential_complex'
        ).prefetch_related(
            'safety', 'other', 'document', 'images', 'real_estate_phones'
        )

        if search_query:
            base_queryset = base_queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(address__icontains=search_query) |
                Q(region__region__icontains=search_query) |
                Q(city__city__icontains=search_query) |
                Q(property_type__icontains=search_query) |
                Q(rooms__name__icontains=search_query) |
                Q(residential_complex__name__icontains=search_query)
            )

        filter_instance = MainPageFilter(request.query_params, queryset=base_queryset)
        filtered_queryset = filter_instance.qs

        latest_objects = filtered_queryset.order_by('-created_at')

        paginator = Paginator(latest_objects, page_size)
        page_obj = paginator.get_page(page)

        serialized_objects = []
        for obj in page_obj:
            if isinstance(obj, ApartmentAd):
                serializer = ApartmentAdSerializer(obj, context={'request': request})
            elif isinstance(obj, HouseAd):
                serializer = HouseAdSerializer(obj, context={'request': request})
            elif isinstance(obj, CommercialAd):
                serializer = CommercialAdSerializer(obj, context={'request': request})
            elif isinstance(obj, RoomAd):
                serializer = RoomAdSerializer(obj, context={'request': request})
            elif isinstance(obj, DachaAd):
                serializer = DachaAdSerializer(obj, context={'request': request})
            elif isinstance(obj, PlotAd):
                serializer = PlotAdSerializer(obj, context={'request': request})
            elif isinstance(obj, ParkingAd):
                serializer = ParkingAdSerializer(obj, context={'request': request})
            
            serialized_objects.append({
                'type': obj.property_type,
                'data': serializer.data
            })

        pagination_info = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'current_page': page,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'next_page': page + 1 if page_obj.has_next() else None,
            'previous_page': page - 1 if page_obj.has_previous() else None
        }

        return Response({
            'results': serialized_objects,
            'pagination': pagination_info
        })
