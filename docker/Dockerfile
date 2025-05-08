FROM apache/airflow:2.10.4-python3.10

USER root

COPY requirements.txt /requirements.txt

USER airflow
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -U -r /requirements.txt