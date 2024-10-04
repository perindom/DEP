import s3fs
from s3fs.core import S3FileSystem
import numpy as np
import pickle

def transform_data():

    s3 = S3FileSystem()
    # S3 bucket directory (data lake)
    DIR = 's3://ece5984-s3-perindom/Lab2/batch_ingest/'
    # Insert your S3 bucket address here. Read from the directory you created in batch ingest: Lab2/batch_ingest/
    # Get data from S3 bucket as a pickle file
    raw_data = np.load(s3.open('{}/{}'.format(DIR, 'data.pkl')), allow_pickle=True)  


    #raw_data = np.load('data.pkl', allow_pickle=True)
    # Dividing the raw dataset for each company individual company
    raw_data.columns = raw_data.columns.swaplevel(0,1)
    raw_data.sort_index(axis=1, level=0, inplace=True)
    df_aapl_rw = raw_data['AAPL']
    df_amzn_rw = raw_data['AMZN']
    df_noc_rw = raw_data['NOC']

    # Dropping rows with NaN in them
    df_aapl = df_aapl_rw.dropna()
    df_amzn = df_amzn_rw.dropna()
    df_noc = df_noc_rw.dropna()


    # Removing rows with outliers
    for col in list(df_aapl.columns)[0:4]:                                          # We ignore 'Volume' column
        df_aapl = df_aapl.drop(df_aapl[df_aapl[col].values > 900].index)            # Values above 900 are dropped
        df_aapl = df_aapl.drop(df_aapl[df_aapl[col].values < 0.001].index)          # Values below 0.001 are dropped

        df_amzn = df_amzn.drop(df_amzn[df_amzn[col].values > 900].index)
        df_amzn = df_amzn.drop(df_amzn[df_amzn[col].values < 0.001].index)

        df_noc = df_noc.drop(df_noc[df_noc[col].values > 900].index)
        df_noc = df_noc.drop(df_noc[df_noc[col].values < 0.001].index)

    # Dropping duplicate rows
    df_aapl = df_aapl.drop_duplicates()
    df_amzn = df_amzn.drop_duplicates()
    df_noc = df_noc.drop_duplicates()

    # Push cleaned data to S3 bucket warehouse
    DIR_wh = 's3://ece5984-s3-perindom/Lab2/transformed'   # Insert your S3 bucket address here. Create a directory as: Lab2/transformed/
    with s3.open('{}/{}'.format(DIR_wh, 'clean_aapl.pkl'), 'wb') as f:
        f.write(pickle.dumps(df_aapl))
    with s3.open('{}/{}'.format(DIR_wh, 'clean_amzn.pkl'), 'wb') as f:
        f.write(pickle.dumps(df_amzn))
    with s3.open('{}/{}'.format(DIR_wh, 'clean_noc.pkl'), 'wb') as f:
        f.write(pickle.dumps(df_noc))


