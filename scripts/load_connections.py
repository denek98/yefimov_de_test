from airflow.models.connection import Connection
from airflow.settings import Session


def create_conn_if_not_exists(conn_id, **kwargs):
    session = Session()
    exists = session.query(Connection).filter_by(conn_id=conn_id).first()
    if exists:
        return
    conn = Connection(conn_id=conn_id, **kwargs)
    session.add(conn)
    session.commit()
    return


create_conn_if_not_exists(
    conn_id="orders_postgres",
    conn_type="postgres",
    host="postgres-1",
    schema="orders_db",
    login="airflow",
    password="airflow",
    port=5432,
)

create_conn_if_not_exists(
    conn_id="orders_eur_postgres",
    conn_type="postgres",
    host="postgres-2",
    schema="orders_eur_db",
    login="airflow",
    password="airflow",
    port=5432,
)
