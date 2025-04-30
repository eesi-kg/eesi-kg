from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.paginator import Paginator
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import (
    ApartmentAd, HouseAd, CommercialAd, RoomAd, 
    DachaAd, PlotAd, ParkingAd, FCMToken
)
from .serializers import (
    ApartmentAdSerializer, HouseAdSerializer, CommercialAdSerializer,
    RoomAdSerializer, DachaAdSerializer, PlotAdSerializer, ParkingAdSerializer,
    FCMTokenSerializer
)
from .filters import (
    ApartmentAdFilter, HouseAdFilter, CommercialAdFilter,
    RoomAdFilter, DachaAdFilter, PlotAdFilter, ParkingAdFilter,
    MainPageFilter
)
from .firebase_service import FirebaseService


class FCMTokenViewSet(viewsets.ModelViewSet):
    serializer_class = FCMTokenSerializer
    http_method_names = ['post', 'delete']

    def get_queryset(self):
        return FCMToken.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Delete any existing tokens for this user and device type
        FCMToken.objects.filter(
            user=self.request.user,
            device_type=serializer.validated_data['device_type']
        ).delete()
        
        # Create new token
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        try:
            token = self.get_object()
            token.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except FCMToken.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class BaseRealEstateViewSet(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        self._send_notification(instance, 'created')
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        self._send_notification(instance, 'updated')
        return instance

    def _send_notification(self, instance, action_type):
        try:
            firebase_service = FirebaseService()
            
            # Get all active FCM tokens
            tokens = FCMToken.objects.filter(is_active=True).values_list('token', flat=True)
            
            if not tokens:
                return

            # Prepare notification data
            title = f"New {instance.get_property_type_display()} {action_type}"
            body = f"{instance.title} - {instance.price} {instance.currency}"
            
            # Additional data to send with notification
            data = {
                'type': 'real_estate',
                'action': action_type,
                'property_type': instance.property_type,
                'public_id': instance.public_id
            }

            # Send notification to all devices
            firebase_service.send_multicast_notification(
                tokens=list(tokens),
                title=title,
                body=body,
                data=data
            )
        except Exception as e:
            logger.error(f"Failed to send notification: {str(e)}")


class ApartmentAdViewSet(BaseRealEstateViewSet):
    queryset = ApartmentAd.objects.filter(is_active=True)
    serializer_class = ApartmentAdSerializer
    filterset_class = ApartmentAdFilter
    lookup_field = 'public_id'


class HouseAdViewSet(BaseRealEstateViewSet):
    queryset = HouseAd.objects.filter(is_active=True)
    serializer_class = HouseAdSerializer
    filterset_class = HouseAdFilter
    lookup_field = 'public_id'


class CommercialAdViewSet(BaseRealEstateViewSet):
    queryset = CommercialAd.objects.filter(is_active=True)
    serializer_class = CommercialAdSerializer
    filterset_class = CommercialAdFilter
    lookup_field = 'public_id'


class RoomAdViewSet(BaseRealEstateViewSet):
    queryset = RoomAd.objects.filter(is_active=True)
    serializer_class = RoomAdSerializer
    filterset_class = RoomAdFilter
    lookup_field = 'public_id'


class DachaAdViewSet(BaseRealEstateViewSet):
    queryset = DachaAd.objects.filter(is_active=True)
    serializer_class = DachaAdSerializer
    filterset_class = DachaAdFilter
    lookup_field = 'public_id'


class PlotAdViewSet(BaseRealEstateViewSet):
    queryset = PlotAd.objects.filter(is_active=True)
    serializer_class = PlotAdSerializer
    filterset_class = PlotAdFilter
    lookup_field = 'public_id'


class ParkingAdViewSet(BaseRealEstateViewSet):
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
