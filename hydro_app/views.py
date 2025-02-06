from rest_framework import viewsets, permissions
from .models import HydroponicSystem, Measurement, ParameterHistory
from .serializers import HydroponicSystemSerializer, MeasurementSerializer, ParameterHistorySerializer, SystemParametersSerializer
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from rest_framework.decorators import action

class MeasurementFilter(filters.FilterSet):
    min_timestamp = filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    max_timestamp = filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')
    min_ph = filters.NumberFilter(field_name='ph', lookup_expr='gte')
    max_ph = filters.NumberFilter(field_name='ph', lookup_expr='lte')
    min_water_temp = filters.NumberFilter(field_name='water_temperature', lookup_expr='gte')
    max_water_temp = filters.NumberFilter(field_name='water_temperature', lookup_expr='lte')
    min_tds = filters.NumberFilter(field_name='tds', lookup_expr='gte')
    max_tds = filters.NumberFilter(field_name='tds', lookup_expr='lte')

    class Meta:
        model = Measurement
        fields = ['hydroponic_system']

class StandardResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class HydroponicSystemViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = HydroponicSystem.objects.all()
    serializer_class = HydroponicSystemSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['name', 'location']
    ordering_fields = ['name', 'location']

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    @action(detail=True, methods=['post'])
    def update_parameters(self, request, pk=None):
        system = self.get_object()
        serializer = SystemParametersSerializer(data=request.data)
        
        if serializer.is_valid():
            measurement_data = {
                'hydroponic_system': system.id,
                **serializer.validated_data
            }
            measurement_serializer = MeasurementSerializer(data=measurement_data)
            if measurement_serializer.is_valid():
                existing_measurements = Measurement.objects.filter(
                    hydroponic_system=system
                ).order_by('-timestamp')
                
                if existing_measurements.count() >= 10:
                    oldest_measurement = existing_measurements.last()
                    oldest_measurement.delete()
                
                measurement_serializer.save()

                for param, value in serializer.validated_data.items():
                    ParameterHistory.objects.create(
                        hydroponic_system=system,
                        parameter_name=param,
                        value=value
                    )

                return Response(measurement_serializer.data)
            return Response(measurement_serializer.errors, status=400)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=['get'])
    def parameter_history(self, request, pk=None):
        system = self.get_object()
        parameters = ['ph', 'water_temperature', 'tds']
        history = {}
        
        for param in parameters:
            history[param] = ParameterHistory.objects.filter(
                hydroponic_system=system,
                parameter_name=param
            )[:10]
            
        serializer = ParameterHistorySerializer(
            [item for sublist in history.values() for item in sublist], 
            many=True
        )
        return Response(serializer.data)

class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = MeasurementFilter
    ordering_fields = ['ph', 'water_temperature', 'tds', 'timestamp']
    pagination_class = StandardResultsPagination

    def get_queryset(self):
        user = self.request.user
        return Measurement.objects.filter(hydroponic_system__owner=user)

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully", "user": UserSerializer(user).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
