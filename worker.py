import json
from kafka import KafkaConsumer
import psycopg2

# Database Configuration
DB_PARAMS = {
    "dbname": "timescale",
    "user": "admin",
    "password": "password",
    "host": "timescaledb",
    "port": "5432"
}

# Kafka Configuration
TOPIC = "color_stream"
BROKER = "kafka:9092"

# Connect to TimescaleDB
conn = psycopg2.connect(**DB_PARAMS)
cursor = conn.cursor()

# Create table if it doesn't exist (including running average column)
cursor.execute("""
CREATE TABLE IF NOT EXISTS color_data (
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    color TEXT,
    value INT,
    running_avg FLOAT
);
""")
conn.commit()

# Subscribe to Kafka
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BROKER,
    auto_offset_reset="earliest",
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# Dictionaries for streaming aggregation
running_totals = {}
running_counts = {}

# Alert threshold
ALERT_THRESHOLD = 90

for msg in consumer:
    data = msg.value
    color = data["color"]
    value = data["value"]

    # Update running average
    if color not in running_totals:
        running_totals[color] = 0
        running_counts[color] = 0

    running_totals[color] += value
    running_counts[color] += 1
    running_avg = running_totals[color] / running_counts[color]

    print(f"Processing: {data} | Running Avg: {running_avg}")

    # Trigger an alert if value exceeds threshold
    if value > ALERT_THRESHOLD:
        print(f"🚨 ALERT: {color} exceeded threshold with value {value}!")

    # Insert data into TimescaleDB
    cursor.execute(
        "INSERT INTO color_data (color, value, running_avg) VALUES (%s, %s, %s)",
        (color, value, running_avg)
    )
    conn.commit()
