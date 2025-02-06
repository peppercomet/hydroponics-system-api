from rest_framework import viewsets, permissions
from .models import HydroponicSystem, Measurement
from .serializers import HydroponicSystemSerializer, MeasurementSerializer
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