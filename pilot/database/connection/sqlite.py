import os
from peewee import SqliteDatabase

def get_sqlite_database():
    # Use a constant or environment variable for the database name to avoid hardcoding it.
    # This makes it easier to manage and change the database name in the future.
    db_name = "my_database.db"
    
    # Use os.path.abspath to ensure the database path is always absolute, making it easier to manage.
    db_path = os.path.abspath(db_name)

    # Peewee's SqliteDatabase function handles the database name safely internally.
    return SqliteDatabase(db_path)

# Initialize the database connection
database = get_sqlite_database()

# Additional code to create models, tables, and perform queries can be added here.
