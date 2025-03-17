
import os
from google.cloud import bigquery
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, trim, regexp_replace, length

# Set Google Cloud authentication with local host
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "big-test-449715-2b0e9010365e.json"


# Google Cloud Project & Dataset Details
PROJECT_ID = "big-test-449715"
DATASET_ID = "LLM"
TABLE_NAME = "review_amazon"

# MongoDB connection details
MONGODB_URI = "mongodb+srv://mostafamoeini77:09197897094%40Mm@pspark-cluster.bazje.mongodb.net/?retryWrites=true&w=majority&appName=Pspark-Cluster"
MONGODB_DATABASE = "preprocessed-review"
MONGODB_COLLECTION = "amazon_reviews"

# Initialize BigQuery client & check authentication
client = bigquery.Client()
datasets = list(client.list_datasets())
if datasets:
    print("BigQuery authentication successful!")
    for dataset in datasets:
        print(f"- {dataset.dataset_id}")
else:
    print("No datasets found, but authentication is working.")

# Initialize Spark session with BigQuery support
spark = SparkSession.builder \
    .appName("AmazonReviewProcessing") \
    .config("spark.jars.packages", "com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.32.2") \
    .config("parentProject", PROJECT_ID) \
    .getOrCreate()

print("PySpark Session Initialized!")

try:
    # Retrieve 100 records from BigQuery into Spark DataFrame
    print("Loading data from BigQuery...")
    df = spark.read.format("bigquery") \
        .option("table", f"{PROJECT_ID}.{DATASET_ID}.{TABLE_NAME}") \
        .option("credentialsFile", "big-test-449715-2b0e9010365e.json") \
        .load() \
        .limit(100)  # Limit to 100 records

    print("Data loaded from BigQuery!")
    print("Original data sample:")
    df.show(5, truncate=False)
    
    # Data Preprocessing: clean text columns
    print("Preprocessing data...")
    df_cleaned = df.withColumn("review", lower(trim(col("review")))) \
                   .withColumn("review", regexp_replace(col("review"), "[^a-zA-Z0-9\\s]", " ")) \
                   .withColumn("review", regexp_replace(col("review"), "\\s+", " ")) \
                   .filter(length(col("review")) > 10) \
                   .withColumn("rating", col("rating").cast("integer")) \
                   .dropna(subset=["review", "rating"])

    print("Data cleaned successfully!")
    print("Processed data sample:")
    df_cleaned.show(5, truncate=False)
    print(f"Number of records after preprocessing: {df_cleaned.count()}")

    # Convert to pandas DataFrame for MongoDB insertion
    pandas_df = df_cleaned.toPandas()
    
    # Connect to MongoDB and insert data
    from pymongo import MongoClient
    
    print("Connecting to MongoDB...")
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DATABASE]
    collection = db[MONGODB_COLLECTION]
    
    # Insert data to MongoDB
    records = pandas_df.to_dict('records')
    if records:
        result = collection.insert_many(records)
        print(f"Successfully inserted {len(result.inserted_ids)} documents to MongoDB database '{MONGODB_DATABASE}', collection '{MONGODB_COLLECTION}'")
    else:
        print("No data to write to MongoDB")
    
    client.close()
    
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Stop Spark session
    spark.stop()
    print("PySpark session stopped")