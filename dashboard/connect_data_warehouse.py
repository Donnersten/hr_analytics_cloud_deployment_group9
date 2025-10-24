from pathlib import Path
import duckdb
import os 
import pandas as pd

FILES_SHARE_PATH = Path("/mnt/data/job_ads.duckdb")
 
def query_job_listings(tabel_name='marts.mart_social_job'):
    query = f'SELECT * FROM {tabel_name}'
    with duckdb.connect(FILES_SHARE_PATH, read_only=True) as conn:
        # return conn.query(f"{query}").df()
        df = pd.read_sql(query, conn)
        return df
