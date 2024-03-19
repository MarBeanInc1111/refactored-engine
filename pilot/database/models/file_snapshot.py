import logging

from peewee import ForeignKeyField, BlobField # Importing necessary classes from peewee ORM

from database.models.components.base_models import BaseModel # Importing BaseModel for inheritance
from database.models.development_steps import DevelopmentSteps
from database.models.app import App
from database.models.files import File

# Initialize the logger
log = logging.getLogger(__name__)


class SmartBlobField(BlobField):
    """
    A custom BlobField that can handle both binary and utf-8 string data.

    This class is a temporary workaround for the fact that we're passing either binary
    or string contents to the database. Once this is cleaned up, we should only
    accept binary content and explcitily convert from/to strings as needed.
    """

    def db_value(self, value):
        """
        Convert utf-8 strings to bytes before storing in the database.

        :param value: The value to be stored in the database
        :return: The converted binary value
        """
        if isinstance(value, str):
            log.warning("FileSnapshot content is a string, expected bytes, working around it.")
            value = value.encode("utf-8")
        return super().db_value(value)

    def python_value(self, value):
        """
        Convert bytes to utf-8 strings when retrieving from the database.

        :param value: The value retrieved from the database
        :return: The decoded utf-8 string or binary value
        """
        val = bytes(super().python_value(value))
        try:
            return val.decode("utf-8")
        except UnicodeDecodeError:
            return val


class FileSnapshot(BaseModel):
    """
    A model representing a snapshot of a File at a specific DevelopmentStep for an App.

    This model is used to store the content of a File at various DevelopmentSteps
    for a given App.
    """

    app = ForeignKeyField(App, on_delete='CASCADE') # Foreign key to the App model
    development_step = ForeignKeyField(DevelopmentSteps, backref='files', on_delete='CASCADE') # Foreign key to the DevelopmentSteps model
    file = ForeignKeyField(File, on_delete='CASCADE', null=True) # Foreign key to the File model, allowing NULL values
    content = SmartBlobField() # The content of the FileSnapshot, stored as a binary
