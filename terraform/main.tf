
provider "google" {
  project     = "big-test-449715"
  region      = "us-central1"
  credentials = file("big-test-449715-2b0e9010365e.json")  # Replace with your actual key filename
}

# Create BigQuery Dataset
resource "google_bigquery_dataset" "llm_dataset" {
  dataset_id    = "LLM"
  friendly_name = "LLM Dataset"
  description   = "Dataset for storing Amazon review data"
  location      = "US"

  # Ignore if the dataset already exists
  lifecycle {
    ignore_changes = [dataset_id]
  }
}

# Create BigQuery Table (if needed)
resource "google_bigquery_table" "amazon_reviews" {
  dataset_id = google_bigquery_dataset.llm_dataset.dataset_id
  table_id   = "review_amazon"

  schema = <<EOF
[
  {"name": "review_id", "type": "STRING"},
  {"name": "product_id", "type": "STRING"},
  {"name": "review_text", "type": "STRING"},
  {"name": "rating", "type": "INTEGER"}
]
EOF

  deletion_protection = false
}

# MongoDB Configuration (Placeholder)
variable "mongodb_uri" {
  default = "mongodb+srv://mostafamoeini77:09197897094%40Mm@pspark-cluster.bazje.mongodb.net/?retryWrites=true&w=majority&appName=Pspark-Cluster"
}

variable "mongodb_database" {
  default = "preprocessed-review"
}

variable "mongodb_collection" {
  default = "amazon_reviews"
}

