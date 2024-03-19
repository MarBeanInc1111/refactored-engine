# Import the `os` module to interact with the operating system
import os

# Set the default database type to SQLite
DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite")
# Get the name of the database from the environment variable `DB_NAME`
DB_NAME = os.getenv("DB_NAME")
# Get the host of the database from the environment variable `DB_HOST`
DB_HOST = os.getenv("DB_HOST")
# Get the port of the database from the environment variable `DB_PORT`
DB_PORT = os.getenv("DB_PORT")
# Get the user of the database from the environment variable `DB_USER`
DB_USER = os.getenv("DB_USER")
# Get the password of the database from the environment variable `DB_PASSWORD`
DB_PASSWORD = os.getenv("DB_PASSWORD")
