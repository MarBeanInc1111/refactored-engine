from peewee import CharField, IntegerField, DateTimeField, DateTimeField as PeeweeDateTimeField
from datetime import datetime, timedelta

from database.models.components.base_models import BaseModel

class User(BaseModel):
    email = CharField(unique=True)
    password = CharField()
    request_count = IntegerField(default=0)
    last_request_time = PeeweeDateTimeField(default=datetime.utcnow)

    def has_exceeded_request_limit(self, max_requests=5, request_interval=timedelta(minutes=1)):
        """Check if the user has exceeded the maximum number of requests within a given interval"""
        if self.request_count >= max_requests:
            return True

        current_time = datetime.utcnow()
        time_diff = current_time - self.last_request_time
        if time_diff < request_interval:
            return True

        self.request_count = 0
        self.last_request_time = current_time
        self.save()
        return False
