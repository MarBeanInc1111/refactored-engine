import os
import pytest
from unittest.mock import patch, MagicMock
from utils.settings import Settings, Loader, expected_config_location

@pytest.fixture
def settings():
    return Settings()

@pytest.fixture
def loader(settings):
    return Loader(settings)


import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from utils.settings import Settings

def test_settings_initializes_known_variables(settings):
    assert settings.openai_api_key == ""
    assert settings.telemetry is None

def test_settings_init_ignores_unknown_variables(settings):
    settings = Settings(unknown="value")
    assert not hasattr(settings, "unknown")

def test_settings_forbids_saving_unknown_variables(settings):
    with pytest.raises(AssertionError):
        settings.unknown = "value"

def test_settings_update(settings):
    settings.update(openai_api_key="test_key")
    assert settings.openai_api_key == "test_key"

def test_settings_to_dict(settings):
    settings.update(openai_api_key="test_key")
    assert dict(settings) == {
        "openai_api_key": "test_key",
        "telemetry": None,
    }


import json
from unittest.mock import patch

import pytest
from utils.settings import Loader, expected_config_location

@patch("utils.settings.open")
@patch("utils.settings.Loader.update_settings_from_env")
def test_loader_load_config_file(_mock_from_env, mock_open, loader):
    fake_config = json.dumps(
        {
            "openai_api_key": "test_key",
            "telemetry": {
                "id": "fake-id",
                "endpoint": "https://example.com",
            },
        }
    )
    mock_open.return_value.__enter__.return_value = fake_config

    loader.load()

    mock_open.assert_called_once_with(loader.config_path, "r", encoding="utf-8")
    assert loader.settings.openai_api_key == "test_key"
    assert loader.settings.telemetry["id"] == "fake-id"
    assert loader.settings.telemetry["endpoint"] == "https://example.com"

@patch("utils.settings.open")
@patch("utils.settings.Loader.update_settings_from_env")
def test_loader_load_no_config_file(_mock_from_env, mock_open, loader):
    loader.config_path = MagicMock()
    loader.config_path.exists.return_value = False
    loader.load()

    loader.config_path.exists.assert_called_once_with()
    mock_open.assert_not_called()
    assert loader.settings.openai_api_key is None
    assert loader.settings.telemetry is None

@patch("utils.settings.getenv")
def test_loader_load_from_env(mock_getenv, loader):
    mock_getenv.side_effect = {
        "OPENAI_API_KEY": "test_key",
        "TELEMETRY_ID": "test_id",
        "TELEMETRY_ENDPOINT": "https://test.com",
    }.get
    loader.update_settings_from_env()

    assert loader.settings.openai_api_key == "test_key"
    assert loader.settings.telemetry["id"] == "test_id"
    assert loader.settings.telemetry["endpoint"] == "https://test.com"


import json
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

class Settings:
    def __init__(self):
        self.openai_api_key = ""
        self.telemetry = None

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self):
        return {key: value for key, value in vars(self).items() if not key.startswith("_")}

class Loader:
    def __init__(self, settings):
        self.settings = settings
        self.config_path = expected_config_location()

    def load(self):
        if self.config_path.exists():
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            self.update_settings_from_dict(config)
        self.update_settings_from_env()

    def update_settings_from_dict(self, config):
        for key, value in config.items():
            setattr(self.settings, key, value)

    def update_settings_from_env(self):
        self.settings.update(
            **{
                key: value
                for key, value in os.environ.items()
                if key.upper() in ["OPENAI_API_KEY", "TELEMETRY_ID", "TELEMETRY_ENDPOINT"]
            }
       
