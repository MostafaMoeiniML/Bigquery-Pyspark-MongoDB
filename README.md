# BigQuery-PySpark-MongoDB Data Engineering Project

This repository contains a data engineering project that involves the use of Docker, Apache Airflow, Terraform, PySpark, BigQuery, and MongoDB. The project is designed for building a robust data pipeline with two microservices and ingest big amazon_review dataset from local host and save it into BigQuery and processes dataset with pyspark and loads data into MongoDB for using sentiment analysis ML app.

## Project Overview

The project includes two microservices and components to handle data ingestion, preprocessing, and processing. This includes:

- **Docker Compose setup** for containerized services.
- **Apache Airflow DAGs** for managing workflows.
- **Terraform** configurations for infrastructure setup.
- **PySpark** scripts for data processing.

## Credentials File

### Location: `credentials/`
The project requires access to Google Cloud services for BigQuery. The credentials file contains sensitive information such as service account keys for Google Cloud. This file is ignored in the repository using `.gitignore` to prevent accidental commits of sensitive data.

### How to Use:
1. Firstly you should download this file **Google Cloud Service Account** (big-test-449715-2b0e9010365e.json) from   (https://drive.google.com/drive/u/4/folders/16qyKNRDmMrKSCbH7vv9_51Ajmy5Byf_A)  google drive address and paste into these folders: microservices_data ingestion, microservices_data preprocessing, terraform .
2. Secondly you should download the dataset from (https://drive.google.com/drive/u/4/folders/16qyKNRDmMrKSCbH7vv9_51Ajmy5Byf_A) and then paste into microservices_data ingestion folder.
3. And you should create two images from Ingestion DockerFile and Preprocessing DockerFile with the following commands , just don't forget firstly go to the path of each microservices and then run these command on the right path:
   a. docker build -t ingestion-microservice     # run this command in the path of microservices_data ingestion
   b. docker build -t preprocess_micro           # run this command in the path of microservices_data preprocessing
4. And then run the docker desktop and build a docker-copmose and up it with the following command:
    - docker compose build                       # run this command in the path of Bigquery-Pyspark-MongoDB
    - docker-compose up
5. And then you can see all logs that shows ingest data from local server and save it into BigQuery and then with another microservices get a part of dataset into Pyspark and preprocess it and then save the cleaned-data into MongoDB.

