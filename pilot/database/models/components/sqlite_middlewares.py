from peewee import *
from peewee_mysql import JSONField


db = MySQLDatabase('database_name', **database_settings)

class MyModel(Model):
    my_json_field = JSONField()

    class Meta:
        database = db

# Usage
my_model = MyModel.create(my_json_field={'key': 'value'})
stored_json = my_model.my_json_field
deserialized_json = my_model.my_json_field
