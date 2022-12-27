from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

#from airflow.providers.amazon.aws.operators.s3 import S3CreateBucketOperator, S3DeleteBucketOperator
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator

with DAG(
    "russia-loss-daily", 
    start_date=datetime.now(),
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

    local_to_s3_equipment = LocalFilesystemToS3Operator(
        task_id="local_to_s3_equipment",
        aws_conn_id='aws_connection',
        replace=True,
        params={
            "file_name": "russia_losses_equipment.csv"
        },
        dest_bucket="russia-losses-2022",
        dest_key="statistics/equipment/{{ params.file_name }}",
        filename="/opt/airflow/dags/datasets/{{ params.file_name }}"
    )

    local_to_s3_personnel = LocalFilesystemToS3Operator(
        task_id="local_to_s3_personnel",
        aws_conn_id='aws_connection',
        replace=True,
        params={
            "file_name": "russia_losses_personnel.csv"
        },
        dest_bucket="russia-losses-2022",
        dest_key="statistics/personnel/{{ params.file_name }}",
        filename="/opt/airflow/dags/datasets/{{ params.file_name }}"
    )

    local_to_s3_correction = LocalFilesystemToS3Operator(
        task_id="local_to_s3_correction",
        aws_conn_id='aws_connection',
        replace=True,
        params={
            "file_name": "russia_losses_equipment_correction.csv"
        },
        dest_bucket="russia-losses-2022",
        dest_key="statistics/equipment_adjustments/{{ params.file_name }}",
        filename="/opt/airflow/dags/datasets/{{ params.file_name }}"
    )

    run_glue_job = GlueJobOperator(
        task_id="run_glue_job",
        aws_conn_id='aws_connection',
        job_name="russia-losses-nb",
        wait_for_completion=True,
        region_name="us-east-1",
        iam_role_name="GlueAccessS3Role",
        create_job_kwargs={
            "GlueVersion": "3.0",
            "NumberOfWorkers": 10, 
            "WorkerType": "G.1X"
            }
    )

    end_operator = EmptyOperator(
        task_id="Stop_Execution"
    )

    start_operator >> kaggle_data_to_local
    kaggle_data_to_local >> [ local_to_s3_equipment, local_to_s3_personnel, local_to_s3_correction]
    [ local_to_s3_equipment, local_to_s3_personnel, local_to_s3_correction] >> run_glue_job
    run_glue_job >> end_operator
