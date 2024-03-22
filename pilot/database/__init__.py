import sqlite3
from pathlib import Path

def database_exists(db_path):
    """Check if the database file exists at the given path."""
    return Path(db_path).exists()

def create_database(db_path):
    """Create a new SQLite database at the given path if it doesn't exist."""
    if not database_exists(db_path):
        with Path(db_path).open('wb') as db_file:
            db_file.write(b'\x00' * 1024 * 1024)  # Write a 1 MB file to avoid creating a zero-byte file.
        print(f"Database '{db_path}' created.")
    else:
        print(f"Database '{db_path}' already exists.")

def connect_to_database(db_path):
    """Connect to the SQLite database at the given path and return a connection object."""
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database '{db_path}': {e}")
        return None

if __name__ == "__main__":
    db_path = "my_database.db"
    create_database(db_path)
    conn = connect_to_database(db_path)
    if conn:
        # Do something with the connection object here.
        pass
