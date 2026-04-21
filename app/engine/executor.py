from app.db.db import get_connection
import pandas as pd

def execute_query(sql):
    conn = get_connection()
    try:
        df = pd.read_sql_query(sql, conn)
        return df
    except Exception as e:
        return str(e)