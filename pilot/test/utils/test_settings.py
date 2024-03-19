# Importing required modules for this module
import json
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Importing functions from the 'utils.settings' module
from utils.settings import Settings, Loader

# Defining a fixture for the expected config location
@pytest.fixture
def expected_config_location():
    platform = sys.platform
    home = os.path.expanduser("~")
    appdata = os.getenv("APPDATA")

    if platform == "darwin" or platform == "linux":
        return os.path.join(home, ".gpt-pilot", "config.json")
    elif platform == "win32":
        return os.path.join(appdata, "GPT Pilot", "config.json")
    else:
        raise RuntimeError(f"Unknown platform: {platform}")

# Test function for checking if Settings initializes known variables
def test_settings_initializes_known_variables():
    settings = Settings()
    assert settings.openai_api_key is None
    assert settings.telemetry is None

# Test function for checking if Settings ignores unknown variables during initialization
def test_settings_init_ignores_unknown_variables():
    settings = Settings(unknown="value")
    assert not hasattr(settings, "unknown")

# Test function for checking if Settings forbids saving unknown variables
def test_settings_forbids_saving_unknown_variables():
    settings = Settings()
    with pytest.raises(AttributeError):
        settings.unknown = "value"

# Test function for checking if Settings update method works as expected
def test_settings_update(settings):
    settings.update(openai_api_key="test_key")
    assert settings.openai_api_key == "test_key"

# Test function for checking if Settings to_dict method works as expected
def test_settings_to_dict(settings):
    settings.update(openai_api_key="test_key")
    assert dict(settings) == {
        "openai_api_key": "test_key",
        "telemetry": None,
    }

# Test function for checking if Loader config_file_location method works as expected
def test_loader_config_file_location(expected_config_location, loader):
    assert loader.config_path == Path(expected_config_location)

# Test function for checking if Loader load_config_file method works as expected
@patch("utils.settings.open")
@patch("utils.settings.Loader.update_settings_from_env")
def test_loader_load_config_file(_mock_from_env, mock_open, expected_config_location, loader):
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
    assert settings.openai_api_key == "test_key"
    assert settings.telemetry["id"] == "fake-id"
    assert settings.telemetry["endpoint"] == "https://example.com"

# Test function for checking if Loader load_no_config_file method works as expected
@patch("utils.settings.open")
@patch("utils.settings.Loader.update_settings_from_env")
def test_loader_load_no_config_file(_mock_from_env, mock_open, expected_config_location, loader):
    loader.config_path = MagicMock()
    loader.config_path.exists.return_value = False
    loader.load()

    loader.config_path.exists.assert_called_once_with()
    mock_open.assert_not_called()
    assert settings.openai_api_key is None
    assert settings.telemetry is None

# Test function for checking if Loader update_settings_from_env method works as expected
@patch("utils.settings.getenv")
def test_loader_load_from_env(mock_getenv, settings):
    mock_getenv.side_effect = {
        "OPENAI_API_KEY": "test_key",
        "TELEMETRY_ID": "test_id",
        "TELEMETRY_ENDPOINT": "https://test.com",
    }.get
    Loader.update_settings_from_env(settings)

    assert settings.openai_api_key == "test_key"
    assert settings.telemetry["id"] == "test_id"
    assert settings.telemetry["endpoint"] == "https://test.com"

# Initializing settings and loader objects for the tests
settings = Settings()
loader = Loader(settings)
