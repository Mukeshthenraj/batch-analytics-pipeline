from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="smoke_test",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    hello_task = BashOperator(
        task_id="hello",
        bash_command="echo 'Airflow is working ✅'",
    )
