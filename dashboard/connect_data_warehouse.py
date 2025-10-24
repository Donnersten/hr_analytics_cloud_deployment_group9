from pathlib import Path
import duckdb
import os 
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DUCKDB_PATH")
 
def query_job_listings(tabel_name='marts.mart_socialjob'):
    query = f'SELECT * FROM {tabel_name}'
    with duckdb.connect(DB_PATH, read_only=True) as conn:
    
       
        # return conn.query(f"{query}").df()
        df = pd.read_sql(query, conn)

        return df
if __name__ == "__main__":
    df = query_job_listings()
    print(df)