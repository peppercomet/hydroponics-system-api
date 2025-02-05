from django.contrib.auth.models import User
from hydro_app.models import HydroponicSystem, Measurement
from django.utils import timezone

def populate_test_data():
    try:
        admin_user = User.objects.get(username='david')
    except User.DoesNotExist:
        print("Error: Superuser 'david' not found. Please create it first.")
        return

    systems_data = [
        {
            "name": "Lettuce Garden",
            "location": "Greenhouse A",
        },
        {
            "name": "Tomato Garden",
            "location": "Greenhouse B",
        },
        {
            "name": "Herb Garden",
            "location": "Greenhouse C",
        }
    ]

    for system_data in systems_data:
        system = HydroponicSystem.objects.create(
            name=system_data["name"],
            location=system_data["location"],
            owner=admin_user
        )
        
        Measurement.objects.create(
            hydroponic_system=system,
            ph=6.5,
            water_temperature=22.0,
            tds=800.0,
            timestamp=timezone.now()
        )
        
        print(f"Created system: {system.name} with initial measurements")

    print("Database population completed successfully!")


if __name__ == "__main__":
    populate_test_data()