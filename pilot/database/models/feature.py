from peewee import ForeignKeyField, CharField, BooleanField, DateTimeField, JSONField
from database.config import DATABASE_TYPE
from database.models.components.base_models import BaseModel
from database.models.app import App
from database.models.development_steps import DevelopmentSteps

class Feature(BaseModel):
    app = ForeignKeyField(App, backref='features', on_delete='CASCADE')
    summary = CharField()

    if DATABASE_TYPE == 'postgres':
        messages = JSONField(null=True)
    else:
        messages = JSONField(null=True)

    previous_step = ForeignKeyField(DevelopmentSteps, column_name='previous_step_id')
    completed = BooleanField(default=False)
    completed_at = DateTimeField(null=True)

    class Meta:
        db_table = 'features'
