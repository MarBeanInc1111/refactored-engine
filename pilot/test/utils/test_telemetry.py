from unittest.mock import patch
import uuid
from utils.telemetry import Telemetry, DEFAULT_ENDPOINT

@patch("utils.telemetry.settings")
def test_telemetry_constructor_with_telemetry_enabled(mock_settings):
    # Test the Telemetry constructor with telemetry enabled in settings
    mock_settings.telemetry = {
        "id": "test-id",
        "endpoint": "test-endpoint",
        "enabled": True,
    }
    telemetry = Telemetry()
    # Check if telemetry is enabled
    assert telemetry.enabled
    # Check if telemetry_id is set correctly
    assert telemetry.telemetry_id == "test-id"
    # Check if endpoint is set correctly
    assert telemetry.endpoint == "test-endpoint"


@patch("utils.telemetry.settings")
def test_telemetry_constructor_with_telemetry_disabled(mock_settings):
    # Test the Telemetry constructor with telemetry disabled in settings
    mock_settings.telemetry = {"id": "existing-id", "enabled": False}
    telemetry = Telemetry()
    # Check if telemetry is disabled
    assert not telemetry.enabled


@patch("utils.telemetry.settings")
def test_telemetry_constructor_with_telemetry_not_configured(mock_settings):
    # Test the Telemetry constructor with no telemetry configuration in settings
    mock_settings.telemetry = None
    telemetry = Telemetry()
    # Check if telemetry is disabled
    assert not telemetry.enabled


@patch("utils.telemetry.config_path", "/path/to/config")
@patch("utils.telemetry.settings")
def test_telemetry_constructor_logging_enabled(mock_settings, caplog):
    # Test the Telemetry constructor logs anonymous telemetry enabled message
    caplog.set_level("DEBUG")
    mock_settings.telemetry = {
        "id": "test-id",
        "endpoint": "test-endpoint",
        "enabled": True,
    }
    Telemetry()
    # Check if the message is in the logs
    assert (
        "Anonymous telemetry enabled (id=test-id), configure or disable it in /path/to/config"
        in caplog.text
    )


@patch("utils.telemetry.sys.platform", "test_platform")
@patch("utils.telemetry.sys.version", "test_version")
@patch("utils.telemetry.version", "test_pilot_version")
def test_clear_data_resets_data(telemetry):
    # Test the clear_data method resets telemetry data
    telemetry.data = {
        "model": "test-model",
        "num_llm_requests": 10,
        "num_llm_tokens": 100,
        "num_steps": 5,
        "elapsed_time": 123.45,
        "end_result": "success",
        "user_feedback": "Great!",
        "user_contact": "user@example.com",
    }
    empty = Telemetry()
    # Check if telemetry data is not equal to empty telemetry data
    assert telemetry.data != empty.data

    telemetry.clear_data()

    # Check if telemetry data is equal to empty telemetry data
    assert telemetry.data == empty.data


def test_clear_data_resets_times(telemetry):
    # Test the clear_data method resets start_time and end_time
    telemetry.start_time = 1234567890
    telemetry.end_time = 1234567895

    telemetry.clear_data()

    # Check if start_time and end_time are reset
    assert telemetry.start_time is None
    assert telemetry.end_time is None


def test_clear_counter_resets_times_but_leaves_data(telemetry):
    # Test the clear_counters method resets start_time and end_time but leaves data
    telemetry.data["model"] = "test-model"
    telemetry.start_time = 1234567890
    telemetry.end_time = 1234567895

    telemetry.clear_counters()

    # Check if data is not reset
    assert telemetry.data["model"] == "test-model"
    # Check if start_time and end_time are reset
    assert telemetry.start_time is None
    assert telemetry.end_time is None


@patch("utils.telemetry.settings")
@patch("utils.telemetry.uuid4", return_value="fake-id")
def test_telemetry_setup_enable(mock_uuid4, mock_settings, telemetry):
    # Test the setup method when telemetry is enabled
    mock_settings.telemetry = {"id": "existing-id", "enabled": False}
    telemetry.setup()

    # Check if uuid4 is called once
    mock_uuid4.assert_called_once()
    # Check if telemetry_id is set correctly
    assert telemetry.telemetry_id == "telemetry-fake-id"
    # Check if settings are updated correctly
    assert mock_settings.telemetry == {
        "id": "telemetry-fake-id",
        "endpoint": DEFAULT_ENDPOINT,
        "enabled": True,
    }


@patch("utils.telemetry.settings")
@patch("utils.telemetry.uuid4")
def test_telemetry_setup_already_enabled(mock_uuid4, mock_settings, telemetry):
    # Test the setup method when telemetry is already enabled
    mock_settings.telemetry = {"id": "existing-id", "enabled": True}
    telemetry.setup()
    # Check if uuid4 is not called
    mock_uuid4.assert_not_called()


@patch("utils.telemetry.settings")
def test_set_updates_data(mock_settings, telemetry):
    # Test the set method updates data
    telemetry.data = {"model": "test-model"}
