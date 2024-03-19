import sqlite3
from pathlib import Path

def database_exists(db_path):
    return Path(db_path).exists()

