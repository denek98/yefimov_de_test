from airflow.decorators import dag, task
from airflow.hooks.postgres_hook import PostgresHook
from datetime import datetime, timedelta
import uuid
import random
from faker import Faker

fake = Faker()
CURRENCIES = ["USD", "EUR", "GBP", "JPY", "UAH", "CAD", "CHF"]


@dag(
    schedule="*/10 * * * *",
    catchup=False,
    start_date=datetime(2025, 1, 1),
    default_args={"retries": 1, "retry_delay": timedelta(minutes=5)},
)
def generate_orders_dag():
    @task
    def generate():
        hook = PostgresHook(postgres_conn_id="orders_postgres")
        conn = hook.get_conn()
        cursor = conn.cursor()
        insert_sql = """
            INSERT INTO orders (order_id, customer_email, order_date, amount, currency)
            VALUES (%s, %s, %s, %s, %s)
        """
        orders = []
        for _ in range(5000):
            orders.append(
                (
                    str(uuid.uuid4()),
                    fake.email(),
                    fake.date_time_between(start_date="-7d", end_date="now"),
                    round(random.uniform(10, 10000), 2),
                    random.choice(CURRENCIES),
                )
            )
        cursor.executemany(insert_sql, orders)
        conn.commit()
        cursor.close()
        conn.close()

    generate()


generate_orders_dag()
