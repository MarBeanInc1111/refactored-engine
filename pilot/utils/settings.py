import ast
import json
from logging import getLogger
from os import getenv, makedirs
from pathlib import Path
import sys
from typing import Any, Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

log = getLogger(__name__)

# List of available settings
AVAILABLE_SETTINGS = [
    "telemetry",
    "openai_api_key",
]


class Settings:
    """
    Application settings class.

    This class holds all the settings for the application, whether they are
    loaded from the config file, set via environment variables or the command
    line arguments.

    Available settings are listed in the `AVAILABLE_SETTINGS` list.

    This is a singleton object, use it by importing the instance
    directly from the module:

    >>> from utils.settings import settings

    To get a setting:

    >>> settings.openai_api_key

    To get all settings as a dictionary:

    >>> dict(settings)

    To set (update) one setting:

    >>> settings.openai_api_key = "test_key"

    To update multiple settings at once:

    >>> settings.update(openai_api_key="test_key", telemetry=None)

    Note: updating settings will not save them to the config file.
    To do that, use the `loader.save()` method:

    >>> from utils.settings import loader
    >>> loader.save("openai_api_key", "telemetry")

    To see all available settings:

    >>> from utils.settings import AVAILABLE_SETTINGS
    >>> print(AVAILABLE_SETTINGS)
    """

    # Available settings
    __slots__ = AVAILABLE_SETTINGS

    def __init__(self, **kwargs):
        """
        Initialize the Settings object.

        Set all settings to None and update them with the provided keyword
        arguments.
        """
        for key in self.__slots__:
            setattr(self, key, None)

        self.update(**kwargs)

    def __iter__(self):
        """
        Iterate over the settings.

        Yield a tuple of the setting name and its value.
        """
        for key in self.__slots__:
            yield key, getattr(self, key)

    def update
