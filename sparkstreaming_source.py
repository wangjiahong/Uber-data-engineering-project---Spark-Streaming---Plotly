import time
import json
import random

def generate_ride_data():
    locations = ['Downtown', 'Airport', 'Suburbs']
    vehicle_types = ['Sedan', 'SUV', 'Luxury']
    payment_types = ['Cash', 'Credit Card', 'PayPal']
    traffic_conditions = ['Light', 'Moderate', 'Heavy']
    weather_conditions = ['Sunny', 'Rainy', 'Snowy']

    while True:
        current_time = time.localtime()
        # Simulate higher frequency during peak hours (7-9 AM and 5-7 PM)
        if (7 <= current_time.tm_hour <= 9) or (17 <= current_time.tm_hour <= 19):
            sleep_time = random.randint(1, 2)
        else:
            sleep_time = random.randint(1, 3)
        
        # Calculate fare based on base fare, distance, and a surge multiplier during peak hours
        distance = round(random.uniform(5, 50), 2)
        base_fare = 2.5
        fare_per_km = 1.75
        surge_multiplier = 2 if sleep_time == 1 else 1
        fare = round(base_fare + (fare_per_km * distance * surge_multiplier), 2)

        ride = {
            'ride_id': random.randint(1000, 9999),
            'driver_id': random.randint(200, 299),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', current_time),
            'fare': fare,
            'location': random.choice(locations),
            'passenger_count': random.randint(1, 4),
            'vehicle_type': random.choice(vehicle_types),
            'trip_duration': random.randint(10, 60),  # Duration in minutes
            'distance': distance,  # Distance in kilometers
            'rating': random.choice([1, 2, 3, 4, 5]),
            'payment_type': random.choice(payment_types),
            'traffic_condition': random.choice(traffic_conditions),
            'weather': random.choice(weather_conditions)
        }
        print(json.dumps(ride))
        time.sleep(0.1)  # More realistic temporal pattern

        # time.sleep(sleep_time)  # More realistic temporal pattern

# To run this function effectively, execute it in a separate Python environment or script.

generate_ride_data()