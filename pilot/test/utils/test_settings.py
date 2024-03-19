# Importing required modules for this module
from io import StringIO
import json
from os.path import expanduser, expandvars, join
from os import getenv
from pathlib import Path
from subprocess import check_output
import sys
from unittest.mock import patch, MagicMock

# Importing functions from the 'utils.settings' module
from utils.settings import (
    Loader,
    Settings,
    get_git_commit,
    get_package_version,
    get_version,
)

# Defining a fixture for the expected config location
@pytest.fixture
def expected_config_location():
    # Getting the XDG_CONFIG_HOME environment variable value
    xdg_config_home = getenv("XDG_CONFIG_HOME")
    # If the variable is set, return the config location based on it
    if xdg_config_home:
        return join(xdg_config_home, "gpt-pilot", "config.json")
    # Based on the platform, return the config location
    elif sys.platform in ["darwin", "linux"]:
        return expanduser("~/.gpt-pilot/config.json")
    elif sys.platform == "win32":
        return expandvars("%APPDATA%\\GPT Pilot\\config.json")
    else:
        # Raise an error if the platform is unknown
        raise RuntimeError(f"Unknown platform: {sys.platform}")

# Test function for checking if Settings initializes known variables
def test_settings_initializes_known_variables():
    settings = Settings()
    # Checking if openai_api_key and telemetry attributes are None
    assert settings.openai_api_key is None
    assert settings.telemetry is None

# Test function for checking if Settings ignores unknown variables during initialization
def test_settings_init_ignores_unknown_variables():
    settings = Settings(unknown="value")
    # Checking if the 'unknown' attribute is not present in the settings object
    assert not hasattr(settings, "unknown")

# Test function for checking if Settings forbids saving unknown variables
def test_settings_forbids_saving_unknown_variables():
    settings = Settings()
    # Trying to set the 'unknown' attribute and checking if it raises AttributeError
    with pytest.raises(AttributeError):
        settings.unknown = "value"

# Test function for checking if Settings update method works as expected
def test_settings_update():
    settings = Settings()
    settings.update(openai_api_key="test_key")
    # Checking if the openai_api_key attribute is updated correctly
    assert settings.openai_api_key == "test_key"

# Test function for checking if Settings to_dict method works as expected
def test_settings_to_dict():
    settings = Settings()
    settings.update(openai_api_key="test_key")
    # Checking if the returned dictionary has the correct keys and values
    assert dict(settings) == {
        "openai_api_key": "test_key",
        "telemetry": None,
    }

# Test function for checking if Loader config_file_location method works as expected
def test_loader_config_file_location(expected_config_location):
    settings = Settings()
    loader = Loader(settings)
    # Checking if the config_path attribute is set correctly
    assert loader.config_path == Path(expected_config_location)

# Test function for checking if Loader load_config_file method works as expected
@patch("utils.settings.open")
@patch("utils.settings.Loader.update_settings_from_env")
def test_loader_load_config_file(_mock_from_env, mock_open, expected_config_location):
    settings = Settings()
    fake_config = json.dumps(
        {
            "openai_api_key": "test_key",
            "telemetry": {
                "id": "fake-id",
                "endpoint": "https://example.com",
            },
        }
    )
    # Mocking the open function and setting the return value
    mock_open.return_value.__enter__.return_value = StringIO(fake_config)

    loader = Loader(settings)
    # Checking if the config_path attribute is set correctly
    assert loader.config_path == Path(expected_config_location)

    loader.config_path = MagicMock()
    loader.load()

    # Checking if the exists method is called on config_path
    loader.config_path.exists.assert_called_once_with()
    # Checking if the open function is called with correct arguments
    mock_open.assert_called_once_with(loader.config_path, "r", encoding="utf-8")

    # Checking if the settings attributes are updated correctly
    assert settings.openai_api_key == "test_key"
    assert settings.telemetry["id"] == "fake-id"
    assert settings.telemetry["endpoint"] == "https://example.com"

# Test function for checking if Loader load_no_config_file method works as expected
@patch("utils.settings.open")
@patch("utils.settings.Loader.update_settings_from_env")
def test_loader_load_no_config_file(_mock_from_env, mock_open, expected_config_location):
    settings = Settings()
    loader = Loader(settings)
    loader.config_path = MagicMock()
    # Setting the exists method to return False
    loader.config_path.exists.return_value = False
    loader.load()

    # Checking if the exists method is called on config_path
    loader.config_path.exists.assert_called_once_with()
    # Checking if the open function is not called
    mock_open.assert_not_called()

    # Checking if the settings attributes are not updated
    assert settings.openai_api_key is None
    assert settings.telemetry is None

# Test function for checking if Loader update_settings_from_env method works as expected
@patch("utils.settings.getenv")
def test_loader_load_from_env(mock
