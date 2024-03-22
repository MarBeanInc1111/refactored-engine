# Import necessary modules and configurations
from database.config import DATABASE_TYPE
from database.models.components.progress_step import ProgressStep
from database.models.components.sqlite_middlewares import JSONField
from playhouse.postgres_ext import BinaryJSONField

# Define a field_type variable based on the DATABASE_TYPE configuration
if DATABASE_TYPE == 'postgres':
    field_type = BinaryJSONField
else:
    field_type = JSONField

# Define the DevelopmentPlanning model as a subclass of ProgressStep
class DevelopmentPlanning(ProgressStep):
    # Declare the development_plan field using the field_type variable
    development_plan = field_type()

    # Declare the Meta class to specify the table name
    class Meta:
        # Set the table name to 'development_planning'
        table_name = 'development_planning'

