from kafka import KafkaProducer
import time
import json
import random

# Setup Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Function to generate mock data
def generate_data():
    return {
        "vehicle_id": random.randint(1000, 9999),
        "speed": round(random.uniform(0, 100), 2),
        "location": {
            "lat": round(random.uniform(-90, 90), 6),
            "lon": round(random.uniform(-180, 180), 6)
        },
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

# Continuously produce data
while True:
    data = generate_data()
    producer.send('mock-data-topic', data)
    print("Produced:", data)
    time.sleep(1)  # send data every second
