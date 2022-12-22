from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

#from airflow.providers.amazon.aws.operators.s3 import S3CreateBucketOperator, S3DeleteBucketOperator
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator


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

    local_to_s3 = LocalFilesystemToS3Operator(
        task_id="Local_to_S3",
        aws_conn_id='aws_connection',
        replace=True,
        dest_bucket="russia-losses-2022",
        dest_key="statistics/2022-ukraine-russian-war.zip",
        filename="/opt/airflow/dags/datasets/2022-ukraine-russian-war.zip"
    )

    end_operator = EmptyOperator(
        task_id="Stop_Execution"
    )

    start_operator >> kaggle_data_to_local
    kaggle_data_to_local >> local_to_s3
    local_to_s3 >> end_operator
