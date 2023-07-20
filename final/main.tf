terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.74.0"
    }
  }
}

variable "service_account_path" {
  type = string
}

variable "service_account_name" {
  type = string
}

variable "project_id" {
  type = string
}

variable "region" {
  type = string
}

variable "function_name" {
  type = string
}

variable "job_name" {
  type = string
}

variable "dataset_id" {
  type = string
}

variable "table_id" {
  type = string
}

variable "bucket_name" {
  type = string
}

variable "table_schema" {
  type = string
}


provider "google" {
  credentials = file(var.service_account_path)
  project     = var.project_id
  region      = var.region
}

resource "google_storage_bucket" "bucket" {
  name = var.bucket_name
  location="us"
}

resource "google_storage_bucket_object" "object" {
  name   = "functions.zip"
  bucket = google_storage_bucket.bucket.name
  source = "functions.zip"  # replace with the actual path to your zip file
}

resource "google_cloudfunctions2_function" "function" {
  name                  = var.function_name
  description           = "Fetches Top Pages and Categories from Wikipedia."
  location              = "us-central1"

  build_config {
    runtime = "python39"
    entry_point = "main"  # Set the entry point 
    source {
      storage_source {
        bucket = google_storage_bucket.bucket.name
        object = google_storage_bucket_object.object.name
      }
    }
  }

  service_config {
    max_instance_count  = 1
    available_memory    = "8Gi"
    timeout_seconds     = 3600
  
  secret_environment_variables {
  key="SECRETKEY"
  secret="wikiSecret"
  version=1
  project_id = var.project_id
  }
  }
}

resource "google_cloud_scheduler_job" "job" {
  name      = var.job_name
  schedule  = "0 7 * * *"
  time_zone = "Europe/London"

  http_target {
    http_method = "GET"
    uri         = google_cloudfunctions2_function.function.service_config[0].uri
  
  oidc_token {
      service_account_email = var.service_account_name
    }
  }
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.dataset_id
}

resource "google_bigquery_table" "table" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = var.table_id

  schema = var.table_schema
}
