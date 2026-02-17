from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="sales_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    generate_data = BashOperator(
        task_id="generate_sales_data",
        bash_command="python /opt/airflow/scripts/generate_sales_data.py"
    )

    validate_data = BashOperator(
        task_id="validate_sales_data",
        bash_command="python /opt/airflow/scripts/validate_sales_data.py"
    )

    upload_to_minio = BashOperator(
        task_id="upload_to_minio",
        bash_command="python /opt/airflow/scripts/upload_to_minio.py"
    )

    load_to_postgres = BashOperator(
        task_id="load_to_postgres",
        bash_command="python /opt/airflow/scripts/load_to_postgres.py"
    )

    generate_data >> validate_data >> upload_to_minio >> load_to_postgres
