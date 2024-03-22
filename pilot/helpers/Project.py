import json
import os
from pathlib import Path
from typing import Tuple

import peewee
from playhouse.shortcuts import model_to_dict

db = peewee.SqliteDatabase('my_database.db')

class BaseModel(peewee.Model):
    class Meta:
        database = db

class User(BaseModel):
    username = peewee.CharField(unique=True)
    email = peewee.CharField(unique=True)

def create_user(username: str, email: str) -> User:
    try:
        user = User.create(username=username, email=email)
        user.save()
    except peewee.IntegrityError as e:
        if 'UNIQUE' in str(e):
            raise ValueError('Username and email must be unique')
        else:
            raise e
    return user

def get_user_by_username(username: str) -> User:
    try:
        return User.get(User.username == username)
    except User.DoesNotExist:
        return None

def get_user_by_email(email: str) -> User:
    try:
        return User.get(User.email == email)
    except User.DoesNotExist:
        return None

def get_all_users() -> Tuple[User]:
    return User.select()

def user_to_dict(user: User) -> dict:
    return model_to_dict(user)

def initialize_database():
    db.connect()
    db.create_tables([User])
    db.close()

if __name__ == '__main__':
    initialize_database()
