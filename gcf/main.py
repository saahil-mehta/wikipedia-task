import functions_framework
from flask import escape
from functions import *
import pandas_gbq

@functions_framework.http
def main(request):
    data = main_process(from_date='2023-07-01',to_date='2023-07-01')
    data.to_gbq(destination_table='dataEngineeringTask.wikiData', if_exists="append")
    return "Data successfully uploaded to BigQuery", 200


print('2023-07-01')
