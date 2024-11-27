import psycopg2
from psycopg2.extras import RealDictCursor

from Intuit.MyBook.src.config.config import POSTGRES_CONFIG


def get_postgres_conn():
    return psycopg2.connect(**POSTGRES_CONFIG)

def get_postgres_cursor(conn):
    return conn.cursor(cursor_factory=RealDictCursor)