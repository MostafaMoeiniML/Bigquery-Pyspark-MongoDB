
import os
import pandas as pd
from google.cloud import bigquery

# Set Google Cloud authentication with container path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/app/credentials.json"

# Set Google Cloud authentication with local host
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "big-test-449715-2b0e9010365e.json"

# Load dataset from local CSV file
# LOCAL_FILE_PATH = "amazon_review.csv"

# Load dataset from local CSV file with container path
LOCAL_FILE_PATH = "/app/amazon_review.csv"
df = pd.read_csv(LOCAL_FILE_PATH)

# Initialize BigQuery client
client = bigquery.Client()

# BigQuery table details
PROJECT_ID = "big-test-449715"
DATASET_ID = "LLM"
TABLE_NAME = "review_amazon"
TABLE_ID = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_NAME}"

# Upload DataFrame to BigQuery
job = client.load_table_from_dataframe(df, TABLE_ID)
job.result()  # Wait for the job to complete

print(f"Data successfully loaded to {TABLE_NAME} in BigQuery!")