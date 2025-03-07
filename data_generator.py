import json
import random
import time
from kafka import KafkaProducer

TOPIC = "color_stream"
BROKER = "kafka:9092"

producer = KafkaProducer(
    bootstrap_servers=BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

colors = ["red", "blue", "green", "yellow"]

while True:
    message = {
        "color": random.choice(colors),
        "value": random.randint(1, 100)
    }
    producer.send(TOPIC, value=message)
    print(f"Published: {message}")
    time.sleep(1)
