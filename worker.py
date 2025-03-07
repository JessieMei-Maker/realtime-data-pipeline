import json
import time
from kafka import KafkaConsumer
import psycopg2

DB_PARAMS = {
    "dbname": "timescale",
    "user": "admin",
    "password": "password",
    "host": "timescaledb",
    "port": "5432"
}

TOPIC = "color_stream"
BROKER = "kafka:9092"

while True:
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        break
    except Exception as e:
        time.sleep(5)

cursor.execute("""
CREATE TABLE IF NOT EXISTS color_data (
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    color TEXT,
    value INT,
    running_avg FLOAT
);
""")
conn.commit()

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BROKER,
    auto_offset_reset="earliest",
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

running_totals = {}
running_counts = {}

for msg in consumer:
    data = msg.value
    color = data["color"]
    value = data["value"]

    if color not in running_totals:
        running_totals[color] = 0
        running_counts[color] = 0

    running_totals[color] += value
    running_counts[color] += 1
    running_avg = running_totals[color] / running_counts[color]

    cursor.execute(
        "INSERT INTO color_data (color, value, running_avg) VALUES (%s, %s, %s)",
        (color, value, running_avg)
    )
    conn.commit()

