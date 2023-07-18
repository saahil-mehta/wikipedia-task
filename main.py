from functions import *
import functions_framework
from pandas import to_gbq

@functions_framework.http
def main(request):
    data = main_process(from_date='2023-04-02',to_date='2023-04-03')
    data.to_gbq(destination_table=dataEngineeringTask.wikiData, if_exists="append")

