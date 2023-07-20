service_account_path = "advancedml-saahil-a12f91c2a1c5.json"
service_account_name = "21784382617-compute@developer.gserviceaccount.com"
project_id           = "advancedml-saahil"
region               = "us-central1"
function_name        = "wikipediaTopPagesFetchv1"
job_name             = "wikiRunSchedulerv1"
dataset_id           = "dataEngineeringTaskv1"
table_id             = "wikipediaTopPages"
bucket_name          = "wiki-scripts-finalv1"
table_schema         = <<EOF
[
  {
    "mode": "NULLABLE",
    "name": "date",
    "type": "STRING"
  },
  {
    "mode": "NULLABLE",
    "name": "article",
    "type": "STRING"
  },
  {
    "mode": "NULLABLE",
    "name": "article_categories",
    "type": "STRING"
  },
  {
    "mode": "NULLABLE",
    "name": "rank",
    "type": "INTEGER"
  },
  {
    "mode": "NULLABLE",
    "name": "views",
    "type": "INTEGER"
  }
]
EOF
