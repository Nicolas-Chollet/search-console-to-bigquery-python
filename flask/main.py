from flask import Flask
from google.oauth2 import service_account
from googleapiclient.discovery import build
import requests
import json
import pandas as pd
from google.cloud import bigquery
from datetime import datetime, timedelta

########### SET YOUR PARAMETERS HERE ####################################
PROPERTIES = ["https://www.unnest.co"]
BQ_DATASET_NAME = 'search_console_demo'
BQ_TABLE_NAME = 'result_table_demo'
SERVICE_ACCOUNT_FILE = 'primeval-door-282907-3cbe2bd9d463.json'
start_date = datetime.strftime(datetime.now() - timedelta(3), '%Y-%m-%d')
end_date = datetime.strftime(datetime.now() - timedelta(3), '%Y-%m-%d')
################ END OF PARAMETERS ######################################

SCOPES = ['https://www.googleapis.com/auth/webmasters']
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build(
    'webmasters',
    'v3',
    credentials=credentials
)


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():

    return end_date

@app.route('/update/', methods=['GET'])
def update():

    def get_sc_df(site_url,start_date,end_date,start_row):
        """Grab Search Console data for the specific property and send it to BigQuery."""

        request = {
          'startDate': start_date,
          'endDate': end_date,
          'dimensions': ['query','device', 'page', 'date'], # uneditable to enforce a nice clean dataframe at the end!
          'rowLimit': 25000,
          'startRow': start_row
           }

        response = service.searchanalytics().query(siteUrl=site_url, body=request).execute()

        if len(response) > 1:

            x = response['rows']

            df = pd.DataFrame.from_dict(x)
            
            # split the keys list into columns
            df[['query','device', 'page', 'date']] = pd.DataFrame(df['keys'].values.tolist(), index= df.index)
            
            # Drop the key columns
            result = df.drop(['keys'],axis=1)

            # Add a website identifier
            result['website'] = site_url

            # establish a BigQuery client
            client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)
            dataset_id = BQ_DATASET_NAME
            table_name = BQ_TABLE_NAME
            # create a job config
            job_config = bigquery.LoadJobConfig()
            # Set the destination table
            table_ref = client.dataset(dataset_id).table(table_name)
            job_config.destination = table_ref
            job_config.write_disposition = 'WRITE_APPEND'

            load_job = client.load_table_from_dataframe(result, table_ref, job_config=job_config)
            load_job.result()

            return result
        else:
            print("There are no more results to return.")

    # Loop through all defined properties, for up to 100,000 rows of data in each
    for p in PROPERTIES:
        for x in range(0,100000,25000):
            y = get_sc_df(p,start_date,end_date,x)
            if len(y) < 25000:
                break
            else:
                continue

    return 'update ok'


if __name__ == '__main__':
    app.run(debug=True)