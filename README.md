# BigQuery-PySpark-MongoDB Data Engineering Project

This repository contains a data engineering project that involves the use of Docker, Apache Airflow, PySpark, BigQuery, and MongoDB. The project is designed for building a robust data pipeline that processes and loads data into BigQuery and MongoDB.

## Project Overview

The project includes several microservices and components to handle data ingestion, preprocessing, and processing. This includes:

- **Docker Compose setup** for containerized services.
- **Apache Airflow DAGs** for managing workflows.
- **Terraform** configurations for infrastructure setup.
- **PySpark** scripts for data processing.

## Credentials File

### Location: `credentials/`
The project requires access to Google Cloud services, including BigQuery, and MongoDB. The credentials file contains sensitive information such as service account keys for Google Cloud. This file is ignored in the repository using `.gitignore` to prevent accidental commits of sensitive data.

### How to Use:

1. Ensure you have a **Google Cloud Service Account** with the appropriate permissions to access BigQuery.
2. Download the **Service Account Key JSON file** from the Google Cloud Console.
3. Place the **Service Account Key JSON file** in the `credentials/` directory.
4. Set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the path of this credentials file.

For example:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials-file.json"
