from flask import Flask, request
from functions import *
import pandas_gbq
import os

app = Flask(__name__)

@app.route('/', methods=['POST'])
def main():
    data = main_process(from_date='2023-04-02',to_date='2023-04-03')
    data.to_gbq(destination_table=dataEngineeringTask.wikiData, if_exists="append")
    return "Data successfully uploaded to BigQuery", 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
