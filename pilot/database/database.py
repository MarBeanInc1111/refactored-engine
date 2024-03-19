import os
import psycopg2
from functools import reduce
from operator import or_
from typing import Any, Dict, List, Optional

import peewee

from const.common import PROMPT_DATA_TO_IGNORE, STEPS
from logger.logger import logger
from database.config import DB_NAME, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DATABASE_TYPE
from database.models.components.base_models import database
from database.models.user import User
from database.models.app import App
from database.models.project_description import ProjectDescription
from database.models.user_stories import UserStories
from database.models.user_tasks import UserTasks
from database.models.architecture import Architecture
from database.models.development_planning import DevelopmentPlanning
from database.models.development_steps import DevelopmentSteps
from database.models.environment_setup import EnvironmentSetup
from database.models.development import Development
from database.models.file_snapshot import FileSnapshot
from database.models.command_runs import CommandRuns
from database.models.user_apps import UserApps
from database.models.user_inputs import UserInputs
from database.models.files import File
from database.models.feature import Feature

TABLES = [
    App,
    ProjectDescription,
    UserStories,
    UserTasks,
    Architecture,
    DevelopmentPlanning,
    DevelopmentSteps,
    EnvironmentSetup,
    Development,
    FileSnapshot,
    CommandRuns,
    UserApps,
    UserInputs,
    File,
    Feature,
]


def connect_database() -> peewee.DatabaseProxy:
    if DATABASE_TYPE == "postgres":
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
    else:
        conn = peewee.SqliteDatabase(None)

    return peewee.DatabaseProxy()(conn)


def get_app(app_id: int, error_if_not_found: bool = True) -> Optional[App]:
    try:
        return App.get(App.id == app_id)
    except App.DoesNotExist:
        if error_if_not_found:
            raise ValueError(f"No app with id: {app_id}")
        return None


# ... (rest of the functions remain unchanged)

def main():
    db = connect_database()
    database.initialize(db)

    if not tables_exist():
        create_tables()


if __name__ == "__main__":
    main()
