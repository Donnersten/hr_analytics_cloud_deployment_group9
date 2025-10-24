from pathlib import Path
import duckdb
import os 
import pandas as pd

DB_PATH = os.getenv("DUCKDB_PATH")
 
def query_job_listings(tabel_name='marts.mart_social_job'):
    query = f'SELECT * FROM {tabel_name}'
    with duckdb.connect(DB_PATH, read_only=True) as conn:
        # return conn.query(f"{query}").df()
        df = pd.read_sql(query, conn)
        return df
