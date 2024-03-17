from peewee import CharField, IntegerField, DateTimeField
from datetime import datetime

from database.models.components.base_models import BaseModel


class User(BaseModel):
    email = CharField(unique=True)
    password = CharField()
    request_count = IntegerField(default=0)
    last_request_time = DateTimeField(default=datetime.utcnow)