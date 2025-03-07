
# Realtime Data Pipeline

This project is a **real-time data pipeline** that streams, processes, and visualizes data using **Kafka, TimescaleDB, and Grafana**.

##  Features

-  **Data Generator:** Generates and sends random messages (JSON format) to Kafka.
- **Kafka Message Bus:** Handles real-time data streaming.
-  **Worker Service:** Processes messages, calculates running averages, and stores results in TimescaleDB.
-  **Grafana Dashboard:** Visualizes real-time data trends.

---

## **1. Prerequisites**

Before running this project, ensure you have:

- **Docker & Docker Compose** installed
- **Git** installed ([Download here](https://git-scm.com/downloads))

---

## 🔧 **2. Installation & Setup**

### **Clone the Repository**

```bash
git clone https://github.com/JessieMei-Maker/realtime-data-pipeline.git
cd realtime-data-pipeline
```

### **Start the Services**

```bash
docker-compose up -d
```

This will start **Kafka, Zookeeper, TimescaleDB, Worker, Data Generator, and Grafana**.

### **Check Running Containers**

```bash
docker ps
```
 Expected output includes **kafka, timescaledb, grafana, worker, data\_generator**.

---

##  **3. Verifying Data Flow**

### **Check Kafka Messages**

```bash
docker exec -it kafka kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic color_stream --from-beginning
```

 Expected output: JSON messages like:

```json
{"color": "red", "value": 42}
```

### **Check Database Entries**

```bash
docker exec -it timescaledb psql -U admin -d timescale -c "SELECT * FROM color_data LIMIT 10;"
```

 Expected output: A table with `timestamp`, `color`, `value`, and `running_avg`.

---

##  **4. Grafana Dashboard Setup**

1. Open **Grafana** in your browser:  [**http://localhost:3000**](http://localhost:3000)
2. **Log in** (default credentials):
   - **Username:** `admin`
   - **Password:** `admin`
3. **Go to "Connections" → "Data Sources"**
4. **Add PostgreSQL** with:
   - **Host:** `timescaledb:5432`
   - **Database:** `timescale`
   - **User:** `admin`
   - **Password:** `password`
5. Click **"Save & Test"**.

### **Create a Dashboard**

1. **Go to "Dashboards" → "New Dashboard"**.
2. **Click "Add a new panel"**.
3. **Enter SQL Query:**
   ```sql
   SELECT time_bucket('1 minute', timestamp) AS time, color, AVG(running_avg) AS avg_value
   FROM color_data
   WHERE timestamp > now() - interval '10 minutes'
   GROUP BY time, color
   ORDER BY time;
   ```
4. Click **"Run Query"** and save the dashboard.

---
