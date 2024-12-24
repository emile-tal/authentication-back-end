import os
from dotenv import load_dotenv
import psycopg
import psycopg.rows

load_dotenv()

def get_db_conn():
    try:
        conn = psycopg.connect(
            host = os.environ['DB_HOST'],
            dbname = os.environ['DB_NAME'],
            user = os.environ['DB_USER'],
            password = os.environ['DB_PASS'],
            port = os.environ['DB_PORT'],
            )
        conn.row_factory = psycopg.rows.dict_row
        return conn
    except Exception as err:
        print(f'Error connecting to database: {err}')

def close_db_conn(conn=None):
    conn.close
