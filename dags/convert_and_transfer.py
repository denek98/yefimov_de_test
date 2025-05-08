from airflow.decorators import dag, task
from airflow.hooks.postgres_hook import PostgresHook
from datetime import datetime, timedelta
import requests
import os


@dag(
    schedule="@hourly",
    catchup=False,
    start_date=datetime(2024, 1, 1),
    default_args={"retries": 1, "retry_delay": timedelta(minutes=5)},
)
def convert_and_transfer_dag():
    """DAG that converts orders to EUR using OpenExchangeRate and loads into another DB.
    Uses 14-day overlap and ON CONFLICT DO NOTHING to avoid missing or duplicating data.
    """

    @task()
    def process_and_load_orders():
        """Fetches recent orders, converts them to EUR, and loads them with conflict handling."""
        if not (APP_ID := os.getenv("APP_ID")):
            raise ValueError("Missing OpenExchangeRate APP_ID")

        response = requests.get(f"https://openexchangerates.org/api/latest.json?app_id={APP_ID}")
        data = response.json()
        if "rates" not in data:
            raise ValueError(f"Invalid response from OpenExchangeRate: {data}")

        rates = data["rates"]
        usd_to_eur = rates["EUR"]

        source_hook = PostgresHook(postgres_conn_id="orders_postgres")
        target_hook = PostgresHook(postgres_conn_id="orders_eur_postgres")

        with source_hook.get_conn() as conn:
            with conn.cursor(name="order_cursor") as cursor:
                cursor.execute(
                    """
                    SELECT order_id, customer_email, order_date, amount, currency
                    FROM orders
                    WHERE order_date >= CURRENT_DATE - INTERVAL '14 days'
                """
                )

                while True:
                    rows = cursor.fetchmany(1000)
                    if not rows:
                        break

                    to_insert = []
                    for row in rows:
                        order_id, email, order_date, amount, currency = row
                        rate = rates.get(currency)
                        if not rate:
                            continue  # skip unknown currency
                        amount_eur = round((float(amount) / rate) * usd_to_eur, 2)
                        to_insert.append((order_id, email, order_date, amount_eur, "EUR"))

                    if to_insert:
                        with target_hook.get_conn() as tgt_conn:
                            with tgt_conn.cursor() as cur:
                                cur.executemany(
                                    """
                                    INSERT INTO orders_eur (order_id, customer_email, order_date, amount, currency)
                                    VALUES (%s, %s, %s, %s, %s)
                                    ON CONFLICT (order_id) DO NOTHING
                                """,
                                    to_insert,
                                )
                            tgt_conn.commit()

    process_and_load_orders()


orders_dag = convert_and_transfer_dag()
