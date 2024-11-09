from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import numpy as np
from s3fs.core import S3FileSystem

def load_data():
    s3 = S3FileSystem()

    # S3 bucket directory (data warehouse)
    DIR_wh = 's3://ece5984-s3-perindom/Lab3' # Insert your data warehouse path from Lab2 - Make sure you remove the "/" from the end of the URI

    # Get data from S3 bucket as pickle files
    aapl_df = np.load(s3.open(f"{DIR_wh}/clean_aapl.pkl"), allow_pickle=True)
    amzn_df = np.load(s3.open(f"{DIR_wh}/clean_amzn.pkl"), allow_pickle=True)
    googl_df = np.load(s3.open(f"{DIR_wh}/clean_googl.pkl"), allow_pickle=True)

    # Create sqlalchemy engine to connect to MySQL
    user = "admin"
    pw = "SE>8qz([p5y<O}9~2wAUl|ld:1ZY" # Update the password to the latest password from db_info.txt file inside EC2 instance
    endpnt = "data-eng-db.cluster-cwgvgleixj0c.us-east-1.rds.amazonaws.com"
    db_name = "perindom" # Name of the database: Insert your PID (email without @vt.edu) here

    # Connect to MySQL server (without specifying a database)
    engine = create_engine(f"mysql+pymysql://{user}:{pw}@{endpnt}")

    # Check if the database already exists
    with engine.connect() as connection:
        db_exists = connection.execute(f"SHOW DATABASES LIKE'{db_name}';").fetchone()
        if not db_exists:
            # Create the database if it does not exist
            connection.execute(f"CREATE DATABASE {db_name}")

    # Reconnect to the specific database
    engine = create_engine(f"mysql+pymysql://{user}:{pw}@{endpnt}/{db_name}")
    # Insert DataFrames into MySQL DB
    aapl_df.to_sql('aapl_clean', con=engine, if_exists='replace', chunksize=1000)
    amzn_df.to_sql('amzn_clean', con=engine, if_exists='replace', chunksize=1000)
    googl_df.to_sql('googl_clean', con=engine, if_exists='replace', chunksize=1000)