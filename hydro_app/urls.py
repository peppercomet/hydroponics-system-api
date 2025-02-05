from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HydroponicSystemViewSet, MeasurementViewSet


router = DefaultRouter()
router.register(r'hydroponic_systems', HydroponicSystemViewSet)
router.register(r'measurements', MeasurementViewSet)


urlpatterns = [
    path('', include(router.urls)),
]