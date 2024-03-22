# Import necessary modules
from peewee import *  # Peewee ORM for working with databases
from database.config import DATABASE_TYPE  # Database type configuration
from database.models.components.progress_step import ProgressStep  # Base progress step model

Field = JSONField if DATABASE_TYPE == 'sqlite' else BinaryJSONField

# Subclass ProgressStep for the Architecture model
class Architecture(ProgressStep):
    # Conditionally define the architecture field based on the database type
    architecture = Field()

    # Define the table name for the Architecture model
    class Meta:
        table_name = 'architecture'
