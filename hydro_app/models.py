from django.contrib.auth.models import User
from django.db import models

# Represents a hydroponic system owned by a user
class HydroponicSystem(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hydroponic_systems")
    
    def __str__(self):
        return self.name

# Represents environmental measurements for a hydroponic system
class Measurement(models.Model):
    hydroponic_system = models.ForeignKey(HydroponicSystem, on_delete=models.CASCADE, related_name="measurements")
    ph = models.FloatField()
    water_temperature = models.FloatField()
    tds = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Measurement for {self.hydroponic_system.name} at {self.timestamp}"

# Represents parameters history for a hydroponic system
class ParameterHistory(models.Model):
    hydroponic_system = models.ForeignKey(HydroponicSystem, on_delete=models.CASCADE, related_name="parameter_history")
    parameter_name = models.CharField(max_length=50)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
