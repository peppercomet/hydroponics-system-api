from rest_framework import serializers
from .models import HydroponicSystem, Measurement

class HydroponicSystemSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = HydroponicSystem
        fields = ['id', 'name', 'location', 'owner']

class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['id', 'hydroponic_system', 'ph', 'water_temperature', 'tds', 'timestamp']