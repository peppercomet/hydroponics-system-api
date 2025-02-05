from rest_framework import serializers
from .models import HydroponicSystem, Measurement
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