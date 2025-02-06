# Hydroponic System API

This is a Django-based project for managing hydroponic systems and storing measurements. It provides a REST API to interact with the systems, measurements, and historical data. The application includes user authentication and token-based authentication for API access.


## Requirements

- Python 3.x
- pip
- Docker (optional)

## Setup
### Using Docker

1. Clone the repository:

   ```bash
   git clone https://github.com/peppercomet/hydroponics-system-api.git
   cd </hydroponics-system-api>
   ```
2. Build and run Docker containers:

   ```bash
   docker-compose up --build
   ```
3. Run migrations

   ```bash
   docker-compose exec web python manage.py migrate
   ```

### Using Python virtual environment

1. Clone the repository:

   ```bash
   git clone https://github.com/peppercomet/hydroponics-system-api.git
   cd </hydroponics-system-api>
   ```
2. Create a Python virtual environment:

   ```bash
   python3 -m venv venv
   ```
3. Activate it

   ```bash
   venv\Scripts\activate
   ```
4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```
5. Apply database migrations:

   ```bash
   python manage.py migrate
   ```
6. Run the Django development server:

   ```bash
   python manage.py runserver
   ```


## Testing the API

I adivse to use curl to interact with the API, for example:
   ```bash
   curl -H "Authorization: Token <token>" http://127.0.0.1:8000/api/hydroponic_systems/
   ```

You can use superuser's token: a63468b22a73c5183ab8b635e16be014aeda6ce7

### Create a Hydroponic System
   ```bash
curl -X POST -H "Authorization: Token <your_token>" -d '{"name": "System 1", "location": "Greenhouse A"}' http://127.0.0.1:8000/api/hydroponic_systems/
   ```

### Read All Hydroponic Systems
   ```bash
curl -H "Authorization: Token <your_token>" http://127.0.0.1:8000/api/hydroponic_systems/
   ```

### Read a Specific Hydroponic System
   ```bash
curl -H "Authorization: Token <your_token>" http://127.0.0.1:8000/api/hydroponic_systems/{id}/
   ```

### Update Hydroponic System Parameters
   ```bash
curl -X POST -H "Authorization: Token <your_token>" -H "Content-Type: application/json" -d "{\"ph\": {x.x}, \"water_temperature\": {y.y}, \"tds\": {zzz.z}}" http://127.0.0.1:8000/api/hydroponic_systems/{id}/update_parameters/
   ```

### Delete a Hydroponic System
   ```bash
curl -X DELETE -H "Authorization: Token <your_token>" http://127.0.0.1:8000/api/hydroponic_systems/{id}/
   ```

### Ordering Parameters
   ```bash
curl -H "Authorization: Token <your_token>" http://127.0.0.1:8000/api/measurements/?ordering=-{parameter}
   ```

where {parameter} might be: {id}, {ph}, {water_temperature}, {timestamp},

### Get Last 10 Measurements
   ```bash
curl -H "Authorization: Token <your_token>" http://127.0.0.1:8000/api/hydroponic_systems/{id}/last_10_measurements/
    ```