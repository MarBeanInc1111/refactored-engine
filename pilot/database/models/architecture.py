# Import necessary modules
from peewee import  # Peewee ORM for working with databases
from database.config import DATABASE_TYPE  # Database type configuration
from database.models.components.progress_step import ProgressStep  # Base progress step model
from database.models.components.sqlite_middlewares import JSONField  # Custom JSON field for SQLite
from playhouse.postgres_ext import BinaryJSONField  # Binary JSON field for PostgreSQL


# Subclass ProgressStep for the Architecture model
class Architecture(ProgressStep):
    # Conditionally define the architecture field based on the database type
    if DATABASE_TYPE == 'postgres':
        architecture = BinaryJSONField()  # Use BinaryJSONField for PostgreSQL
    else:
        architecture = JSONField()  # Use JSONField for SQLite

    # Define the table name for the Architecture model
    class Meta:
        table_name = 'architecture'
