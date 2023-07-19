import functions_framework
from functions import *
import pandas_gbq
import os

@functions_framework.http
def main(request):
    """
    Google Cloud Function HTTP trigger that extracts Wikipedia page view data 
    and uploads it to Google BigQuery.

    This function is triggered by HTTP requests. It first calls the 
    `main_process` function with the start date and end date provision as optional,
    default set to None (which will inturn be defaulted to the start date according to the function definition). 
    It then uploads the resulting data to a BigQuery table named 'dataEngineeringTask.wikiDataNormal'. 
    If the table already exists, the data will be appended to it.

    Parameters
    ----------
    request: flask.Request object
        Incoming HTTP request that triggered the function.
        This parameter is not used in the function, as it does not depend 
        on the contents of the request.

    Returns
    -------
    tuple
        A tuple containing a string message indicating the successful 
        upload of data and an HTTP status code.
    """
    data = main_process(from_date='2023-04-01',to_date=None)
    data.to_gbq(destination_table='dataEngineeringTask.wikiDataNormal', if_exists="append")
    return "Data successfully uploaded to BigQuery", 200
