import os
from google.cloud import bigquery
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, trim, regexp_replace, length
from pymongo import MongoClient
import pandas as pd

# Load Google Cloud Credentials from environment variable
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "/app/credentials.json")

# Google Cloud Project & Dataset Details
PROJECT_ID = "big-test-449715"
DATASET_ID = "LLM"
TABLE_NAME = "review_amazon"

# MongoDB connection details
MONGODB_URI = "mongodb+srv://mostafamoeini77:09197897094%40Mm@pspark-cluster.bazje.mongodb.net/?retryWrites=true&w=majority&appName=Pspark-Cluster"
MONGODB_DATABASE = "preprocessed-review"
MONGODB_COLLECTION = "amazon_reviews"

# Initialize BigQuery client
client = bigquery.Client()

# Initialize Spark session with BigQuery support
spark = SparkSession.builder \
    .appName("AmazonReviewProcessing") \
    .config("spark.jars.packages", "com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.32.2") \
    .config("credentialsFile", GOOGLE_CREDENTIALS_PATH) \
    .getOrCreate()

try:
    print("Loading data from BigQuery...")
    df = spark.read.format("bigquery") \
        .option("table", f"{PROJECT_ID}.{DATASET_ID}.{TABLE_NAME}") \
        .load() \
        .limit(100)

    print("Data loaded! Cleaning now...")
    df_cleaned = df.withColumn("review", lower(trim(col("review")))) \
                   .withColumn("review", regexp_replace(col("review"), "[^a-zA-Z0-9\\s]", " ")) \
                   .withColumn("review", regexp_replace(col("review"), "\\s+", " ")) \
                   .filter(length(col("review")) > 10) \
                   .withColumn("rating", col("rating").cast("integer")) \
                   .dropna(subset=["review", "rating"])

    pandas_df = df_cleaned.toPandas()
    
    print("Connecting to MongoDB...")
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DATABASE]
    collection = db[MONGODB_COLLECTION]
    if not pandas_df.empty:
        collection.insert_many(pandas_df.to_dict('records'))
        print(f"Inserted {len(pandas_df)} records into MongoDB")
    else:
        print("No data to insert")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    spark.stop()
    print("PySpark session stopped")
