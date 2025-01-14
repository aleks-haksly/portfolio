import os
from sqlalchemy import create_engine, text
import pandas as pd

try:
    from utils import env_add
except ImportError:
    # Optionally, log or handle the absence of `env_add` if necessary
    # This needs for local test only. When run id Docker ENV variable 'supabase' for database connection must be set
    pass

# Initialize SQLAlchemy engine using the Supabase connection string
engine = create_engine(os.environ.get("dbconnect"), client_encoding='utf8')

def select(sql: str) -> pd.DataFrame:
    """
    Execute a SQL SELECT query and return the result as a Pandas DataFrame.

    Args:
        sql (str): The SQL query to execute.

    Returns:
        pd.DataFrame: Query results as a DataFrame.
    """
    sql = text(sql)
    return pd.read_sql(sql, engine)

