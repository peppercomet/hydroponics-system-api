from rest_framework import serializers
from .models import HydroponicSystem, Measurement, ParameterHistory
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class HydroponicSystemSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = HydroponicSystem
        fields = ['id', 'name', 'location', 'owner']

class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['id', 'hydroponic_system', 'ph', 'water_temperature', 'tds', 'timestamp']

class ParameterHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ParameterHistory
        fields = ['parameter_name', 'value', 'timestamp']

class SystemParametersSerializer(serializers.Serializer):
    ph = serializers.FloatField(required=False)
    water_temperature = serializers.FloatField(required=False)
    tds = serializers.FloatField(required=False)