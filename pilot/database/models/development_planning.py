# Import necessary modules and configurations
from database.config import DATABASE_TYPE
from database.models.components.progress_step import ProgressStep
from database.models.components.sqlite_middlewares import JSONField
from playhouse.postgres_ext import BinaryJSONField

if DATABASE_TYPE == 'postgres':
    field_type = BinaryJSONField
else:
    field_type = JSONField

class DevelopmentPlanning(ProgressStep):
    development_plan = field_type()

    class Meta:
        table_name = 'development_planning'
