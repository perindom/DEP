import s3fs
from s3fs.core import S3FileSystem
import numpy as np
import pickle
import pandas as pd
from datetime import datetime
import fastf1

def ingest_data():

    df = fastf1.get_event_schedule(2024)

    # Convert 'EventDate' to datetime format
    df['EventDate'] = pd.to_datetime(df['EventDate'])

    # Get today's date
    today = pd.to_datetime(datetime.today().date())

    # Filter rows where EventDate is less than or equal to today's date
    df_recent = df[df['EventDate'] <= today]

    # Find the row with the maximum EventDate
    most_recent_row = df_recent.loc[df_recent['EventDate'].idxmax()]

    session = fastf1.get_session(most_recent_row['EventDate'].year, most_recent_row['Location'], 'Race')
    session.load()
    results = session.results
    results.to_json('data.json')

    s3 = S3FileSystem()

    # S3 bucket directory
    DIR = 's3://ece5984-s3-perindom/Lab1/f1' # insert your S3 URI here... DONE

    # Push data to S3 bucket as a pickle file
    with s3.open('{}/{}'.format(DIR, 'data.pkl'), 'wb') as f:
        f.write(pickle.dumps(data))
        print('sending f1 data to s3')

if __name__ == "__main__":
    ingest_data()
