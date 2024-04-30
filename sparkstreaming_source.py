import time
import json
import random

def generate_ride_data():
    locations = ['Downtown', 'Airport', 'Suburbs']
    vehicle_types = ['Sedan', 'SUV', 'Luxury']
    payment_types = ['Cash', 'Credit Card', 'PayPal']
    traffic_conditions = ['Light', 'Moderate', 'Heavy']
    weather_conditions = ['Sunny', 'Rainy', 'Snowy']
    starting_locations = [
        {"name": "Brooklyn Bridge", "coords": [40.7061, -73.9969]},
        {"name": "Empire State Building", "coords": [40.748817, -73.985428]},
        {"name": "Rockefeller Center", "coords": [40.7587, -73.9787]},
        {"name": "Metropolitan Museum of Art", "coords": [40.779437, -73.963244]},
        {"name": "One World Trade Center", "coords": [40.712743, -74.013379]},
        {"name": "Broadway", "coords": [40.7590, -73.9845]},
        {"name": "Fifth Avenue", "coords": [40.7746, -73.9653]},
        {"name": "Wall Street", "coords": [40.7074, -74.0113]},
        {"name": "Chrysler Building", "coords": [40.7516, -73.9755]},
        {"name": "Grand Central Terminal", "coords": [40.7527, -73.9772]},
        {"name": "Madison Square Garden", "coords": [40.7505, -73.9934]},
        {"name": "High Line", "coords": [40.747993, -74.004765]},

        # Add more locations as needed
    ]

    while True:
        current_time = time.localtime()
        if (7 <= current_time.tm_hour <= 9) or (17 <= current_time.tm_hour <= 19):
            sleep_time = random.randint(1, 2)
        else:
            sleep_time = random.randint(1, 3)
        
        distance = round(random.uniform(5, 50), 2)
        base_fare = 2.5
        fare_per_km = 1.75
        surge_multiplier = 2 if sleep_time == 1 else 1
        fare = round(base_fare + (fare_per_km * distance * surge_multiplier), 2)

        selected_location = random.choice(starting_locations)
        
        ride = {
            'ride_id': random.randint(1000, 9999),
            'driver_id': random.randint(200, 299),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', current_time),
            'fare': fare,
            'location': random.choice(locations),
            'passenger_count': random.randint(1, 4),
            'vehicle_type': random.choice(vehicle_types),
            'trip_duration': random.randint(10, 60),
            'distance': distance,
            'rating': random.choice([1, 2, 3, 4, 5]),
            'payment_type': random.choice(payment_types),
            'traffic_condition': random.choice(traffic_conditions),
            'weather': random.choice(weather_conditions),
            'starting_location_name': selected_location['name'],
            'starting_location_lat': selected_location['coords'][0],
            'starting_location_lon': selected_location['coords'][1]
        }
        print(json.dumps(ride))
        time.sleep(0.1)

generate_ride_data()
