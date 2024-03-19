from peewee import TextField
from database.models.components.progress_step import ProgressStep

class ProjectDescription(ProgressStep):
    """
    A model class that represents a project description in the database.
    Inherits from ProgressStep model class.
    """
    prompt = TextField()
    """
    A text field that stores the prompt for the project description.
    """
    summary = TextField()
    """
    A text field that stores the summary of the project description.
    """

    class Meta:
        """
        Meta class that specifies the name of the table in the database.
        """
        table_name = 'project_description'
