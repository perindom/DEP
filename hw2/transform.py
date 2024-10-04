import s3fs
from s3fs.core import S3FileSystem
import numpy as np
import pickle
import pandas as pd
def transform_data():

    s3 = S3FileSystem()
    # S3 bucket directory (data lake)
    DIR = 's3://ece5984-s3-perindom/hw2/batch_ingested'
    # Insert your S3 bucket address here. Read from the directory you created in batch ingest: Lab2/batch_ingest/
    # Get data from S3 bucket as a pickle file
    df  = np.load(s3.open('{}/{}'.format(DIR, 'data.pkl')), allow_pickle=True)  
    # Remove any empty entries, which could be teams that have no drivers if they erroneously entered the dataframe
    df.dropna()

    # Separate the teams into their own dataframes and extract relevant information
    # Creating the dictionary structure with each team name as a key
    team_dfs = {}

    # Iterating through the unique team names
    for team in df['TeamName'].unique():
        # Filter the DataFrame for the current team
        team_df = df[df['TeamName'] == team]

        # Extract the relevant information
        avg_position = team_df['Position'].mean()
        team_color = team_df['TeamColor'].iloc[0]
        team_id = team_df['TeamId'].iloc[0]

        # Creating the new DataFrame for the team
        team_summary_df = pd.DataFrame({
            'AvgPosition': [avg_position],
            'TeamColor': [team_color],
            'TeamId': [team_id],
        })

        # Adding the new DataFrame to the dictionary
        team_dfs[team] = team_summary_df

    # Push cleaned data to S3 bucket warehouse
    DIR_wh = 's3://ece5984-s3-perindom/hw2/transformed'   # Insert your S3 bucket address here. Create a directory as: Lab2/transformed/
    for name, df_team in team_dfs.items():
        with s3.open('{}/{}'.format(DIR_wh, f'{name}_data.pkl'), 'wb') as f:
            f.write(pickle.dumps(df_team))
