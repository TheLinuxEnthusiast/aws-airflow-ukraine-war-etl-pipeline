from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

#from operators.local_to_s3 import LocalToS3

with DAG(
    "russia-loss-daily", 
    start_date=datetime(2022, 12, 20),
    schedule="@daily",
    catchup=False
) as dag:
    start_operator = EmptyOperator(
        task_id="Start_Execution"
    )

    kaggle_data_to_local = BashOperator(
        task_id="Kaggle_Data_To_Local",
        bash_command="/opt/airflow/plugins/scripts/kaggle_russia_daily_loss.sh "
    )

    #local_to_s3 = LocalToS3(
    #    task_id="Local_to_S3"
    #)

    end_operator = EmptyOperator(
        task_id="Stop_Execution"
    )

    start_operator >> kaggle_data_to_local
    kaggle_data_to_local >> end_operator #local_to_s3
    #local_to_s3 >> end_operator
