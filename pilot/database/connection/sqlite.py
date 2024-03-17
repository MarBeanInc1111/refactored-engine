from peewee import SqliteDatabase
from database.config import DB_NAME

def get_sqlite_database():
    # Ensure that the database name is properly escaped to prevent SQL injection.
    # However, since the database name comes from a configuration file and not from user input,
    # the risk is minimal. Still, it's a good practice to avoid directly using the string.
    # Peewee's SqliteDatabase function handles the database name safely internally.
    return SqliteDatabase(DB_NAME)