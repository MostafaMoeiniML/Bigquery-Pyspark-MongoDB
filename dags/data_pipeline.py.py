from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import requests
import os
from dateutil.relativedelta import relativedelta

# Determine if current run is at quarter end
def is_quarter_end():
    current_month = datetime.now().month
    return current_month in [3, 6, 9, 12]

# Function to trigger ingestion microservice
def trigger_ingestion_service(**kwargs):
    """Trigger the ingestion microservice via HTTP request"""
    ingestion_host = os.getenv('INGESTION_SERVICE_HOST', 'ingestion')
    response = requests.post(f"http://{ingestion_host}:8000/trigger-ingestion")
    
    if response.status_code != 200:
        raise Exception(f"Ingestion service failed with status code: {response.status_code}")
    
    # Store the response data for downstream tasks
    kwargs['ti'].xcom_push(key='ingestion_result', value=response.json())
    
    return response.json()

# Function to trigger preprocessing microservice
def trigger_preprocessing_service(**kwargs):
    """Trigger the preprocessing microservice via HTTP request with quarterly flag"""
    preprocessing_host = os.getenv('PREPROCESSING_SERVICE_HOST', 'preprocessing')
    
    # Check if it's a quarter end
    quarter_end = is_quarter_end()
    
    # Get data from ingestion step
    ti = kwargs['ti']
    ingestion_result = ti.xcom_pull(task_ids='ingest_data', key='ingestion_result')
    
    # Call preprocessing with quarter_end flag
    response = requests.post(
        f"http://{preprocessing_host}:8001/trigger-preprocessing",
        json={
            'quarter_end': quarter_end,
            'ingestion_data': ingestion_result
        }
    )
    
    if response.status_code != 200:
        raise Exception(f"Preprocessing service failed with status code: {response.status_code}")
    
    return response.json()

# Default arguments for the DAG
default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG
dag = DAG(
    'data_pipeline',
    default_args=default_args,
    description='Monthly data ingestion with quarterly delivery',
    # Monthly schedule (runs on the 1st of each month)
    schedule_interval='0 0 1 * *',
    start_date=days_ago(1),
    catchup=False,
)

# Task to trigger ingestion microservice
ingest_task = PythonOperator(
    task_id='ingest_data',
    python_callable=trigger_ingestion_service,
    provide_context=True,
    dag=dag,
)

# Task to trigger preprocessing microservice
preprocess_task = PythonOperator(
    task_id='process_data',
    python_callable=trigger_preprocessing_service,
    provide_context=True,
    dag=dag,
)

# Define task dependencies
ingest_task >> preprocess_task