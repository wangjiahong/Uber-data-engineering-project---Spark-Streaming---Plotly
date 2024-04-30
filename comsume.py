from kafka import KafkaConsumer
import json

# Setup Kafka consumer
consumer = KafkaConsumer(
    'mock-data-topic',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',  # start reading at the earliest message
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Consume data
for message in consumer:
    print("Consumed:", message.value)
