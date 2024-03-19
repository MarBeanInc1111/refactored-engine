# Import necessary modules and configurations
from database.config import DATABASE_TYPE
from database.models.components.progress_step import ProgressStep
from database.models.components.sqlite_middlewares import JSONField

# In case the database is PostgreSQL, use the PostgreSQL JSONField
if DATABASE_TYPE == 'postgres':
    # Import BinaryJSONField from Playhouse's PostgreSQL extensions
    from playhouse.postgres_ext import BinaryJSONField

    class DevelopmentPlanning(ProgressStep):
        development_plan = BinaryJSONField()

# If the database is not PostgreSQL (e.g., SQLite), use the custom JSONField
else:
    class DevelopmentPlanning(ProgressStep):
        development_plan = JSONField()  # Custom JSON field for SQLite

# Define the table name for the DevelopmentPlanning model
class Meta:
    table_name = 'development_planning'
