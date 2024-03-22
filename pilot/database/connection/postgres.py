from peewee import PostgresqlDatabase
from database.config import DB_NAME, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DATABASE_TYPE
import psycopg2
from psycopg2.extensions import quote_ident

def get_postgres_database():
    """Returns a PostgresqlDatabase instance configured with the given settings."""
    return PostgresqlDatabase(DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)

def create_postgres_database():
    """Creates a new PostgreSQL database with the given settings if it doesn't already exist.

    Returns True if the database was created, False if it already existed.
    """
    conn = psycopg2.connect(
        dbname='postgres',
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = True
    cursor = conn.cursor()
    safe_db_name = quote_ident(DB_NAME, conn)

    # Check if the database already exists
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (safe_db_name,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return False

    # Create the database
    try:
        cursor.execute("CREATE DATABASE %s", (safe_db_name,))
    except psycopg2.Error as e:
        cursor.close()
        conn.close()
        raise

    cursor.close()
    conn.close()
    return True

def connect_to_database():
    """Returns a
