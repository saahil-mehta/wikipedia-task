# Technical Documentation

## Objective

The objective of this project is to set up a scheduled ingestion process that performs the following tasks:

- Identify the top 100 most viewed Wikipedia pages for a specified date using the Wikimedia API.
- Extract the associated "categories" for each page in the daily top 100 using the Wikipedia API.
- Save this information in BigQuery.
- Configure the process to run once a day.
- Backfill the data from April 1st, 2023, to the present.

## Implementation

The implementation consists of two main Python files: `main.py` and `functions.py`.

### Code Files

#### main.py

This file contains the main function that triggers the data extraction and upload process. It calls the `main_process` function with the start date and end date provided as optional parameters. The resulting data is then uploaded to a BigQuery table named 'dataEngineeringTask.wikiDataNormal'. If the table already exists, the data will be appended to it.

#### functions.py

This file contains several helper functions that are used to extract and process the data. These include functions to get page view data from the Wikimedia API, generate a list of dates, process a range of dates to get page view data, get categories for a Wikipedia page, process a dataframe to get categories for each article, and a main processing function to get the final dataframe.

### Config

The Google Cloud Function (GCF) is configured with the following settings:

- Region: us-central1
- Memory allocated: 8 GiB
- CPU: 2
- Timeout: 3,600 seconds
- Minimum instances: 0
- Maximum instances: 1
- Concurrency: 1
- Service account: 21784382617-compute@developer.gserviceaccount.com

### Workflow

The entire workflow is built using Terraform HCL IaC and has been tested for robust functionality. The code is written in Python using the highest standards of efficiency and also adhering to scalability and reproducibility by addition of detailed doc strings.

## Failsafe or Backup (backfill.html)

In addition to the main implementation, a local backfill notebook has been created as a failsafe measure. This notebook can be run locally and serves two main purposes:

1. Backup: In case of any failure or disruption in the main pipeline (Cloud Function, Scheduler, or BigQuery), this notebook can be used to manually extract the data and upload it to BigQuery. This ensures that the data ingestion process can continue uninterrupted even in the face of unforeseen issues with the main pipeline.

2. Local Run: The notebook can also be used for local testing and development. For example, if there are any changes or updates to the data extraction and processing logic, these can be first tested locally using the notebook before updating the main pipeline.

The notebook contains the same Python code for data extraction and processing as the main pipeline. It requires the same environment variables (such as the API secret key) and Python libraries as specified in the `requirements.txt` file, however there are some minor tweaks. 

Please note that while the notebook provides a valuable backup, it requires manual intervention to run. Therefore, it's crucial to monitor the main pipeline regularly to detect any issues early and either fix them or switch to the backup notebook as needed.


## Future Improvements

While the current architecture allows for a good amount of scalability due to the use of Terraform, further development could include the use of Google Cloud Build and Cloud Run. However, for a singular routine task such as this, it might be an overkill. A simpler alternative could be a Compute Engine VM with only the required scripts and API key as an environment variable.


