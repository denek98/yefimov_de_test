## Project Overview

This project simulates a real-time order ingestion and conversion pipeline using **Apache Airflow**, **PostgreSQL**, and **OpenExchangeRate API**.

### Features:
- Generates 5000 random orders every 10 minutes (`postgres-1`).
- Every hour, reads orders for the last 14 days and converts amounts to EUR.
- Converted data is saved into `postgres-2.orders_eur`.
- Handles downtimes by 14 days overlap

---



## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/denek98/yefimov_de_test
cd yefimov_de_test
```

### 2. Set up Environment

Add OpenExchange APP_ID to `.env` file:
```dotenv
APP_ID=penexchangerate_app_id
```

### 3. Start Airflow + Postgres with Docker Compose
```bash
docker-compose up --build -d
```

This will start:
- Airflow Scheduler & Webserver
- PostgreSQL (`postgres-1`, `postgres-2`)
- Load initial Airflow connections

Access the Airflow UI: [http://localhost:8080](http://localhost:8080)

Login (default):
- Username: `airflow`
- Password: `airflow`

---

## Airflow DAGs

| DAG ID                  | Schedule     | Description                                |
|------------------------|--------------|--------------------------------------------|
| `generate_orders_dag`  | Every 10 min | Generates 5000 random orders               |
| `convert_and_transfer` | Hourly       | Converts orders to EUR and stores results  |

---

## PostgreSQL Tables

### postgres-1
- `orders`: Raw incoming orders

### postgres-2
- `orders_eur`: Converted orders in EUR
