# Import necessary modules and classes from peewee, the database configuration,
# base models, SQLite middlewares, and Playhouse Postgres Ext for handling
# PostgreSQL-specific fields.
from peewee import ForeignKeyField, AutoField, TextField, IntegerField, CharField
from database.config import DATABASE_TYPE
from database.models.components.base_models import BaseModel
from database.models.app import App
from database.models.components.sqlite_middlewares import JSONField
from playhouse.postgres_ext import BinaryJSONField


# Define the DevelopmentSteps model, which inherits from the BaseModel.
class DevelopmentSteps(BaseModel):
    # Declare the id field as an AutoField, which will serve as the primary key.
    id = AutoField()  # This will serve as the primary key

    # Define a ForeignKeyField for the App model, which will be linked to this
    # DevelopmentSteps model. The 'on_delete' argument is set to 'CASCADE',
    # meaning that if an App is deleted, all associated DevelopmentSteps will
    # also be deleted.
    app = ForeignKeyField(App, on_delete='CASCADE')

    # Declare a TextField for prompt_path, which can store large amounts of text
    # and is set to nullable.
    prompt_path = TextField(null=True)

    # Declare an IntegerField for llm_req_num, which can store integer values
    # and is set to nullable.
    llm_req_num = IntegerField(null=True)

    # Declare a TextField for token_limit_exception_raised, which can store
    # large amounts of text and is set to nullable.
    token_limit_exception_raised = TextField(null=True)

    # If the DATABASE_TYPE is PostgreSQL, use BinaryJSONField for messages,
    # llm_response, and prompt_data. Otherwise, use the custom JSONField for
    # SQLite.
    if DATABASE_TYPE == 'postgres':
        messages = BinaryJSON
