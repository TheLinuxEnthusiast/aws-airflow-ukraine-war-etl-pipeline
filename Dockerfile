FROM apache/airflow:2.4.1

# Install unzip
USER root
RUN apt-get update && apt-get install -y unzip

USER airflow

COPY requirements.txt /requirements.txt

RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r /requirements.txt