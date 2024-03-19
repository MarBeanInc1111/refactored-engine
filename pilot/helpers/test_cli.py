import platform  # Importing platform module to get system information
from unittest.mock import patch, MagicMock, call  # Importing patch, MagicMock, and call from unittest.mock for testing purposes

import pytest  # Pytest library for testing

from helpers.cli import execute_command, terminate_process, run_command_until_success  # Importing functions from helpers.cli module
from helpers.test_Project import create_project  # Importing create_project function from helpers.test_Project module

@pytest.mark.xfail  # Marking the test case as expected to fail
@patch("helpers.cli.os")  # Patching os module
@patch("helpers.cli.subprocess")  # Patching subprocess module
def test_terminate_process_not_running(mock_subprocess, mock_os):  # Test function for terminate_process when process is not running
    terminate_process(1234, 'not running')  # Calling terminate_process with process id and 'not running' message

    mock_subprocess.run.assert_not_called()  # Asserting that subprocess.run was not called
    mock_os.killpg.assert_not_called()  # Asserting that os.killpg was not called

@patch("helpers.cli.MIN_COMMAND_RUN_TIME", create=True, new=100)  # Patching MIN_COMMAND_RUN_TIME with a value of 100
@patch('helpers.cli.run_command')  # Patching run_command function
@patch("helpers.cli.terminate_process")  # Patching terminate_process function
def test_execute_command_timeout_exit_code(mock_terminate_process, mock_run):  # Test function for execute_command when command times out
    # Given
    project = create_project()  # Creating a project
    command = 'cat'  # Command to be executed
    timeout = 0.1  # Timeout value
    mock_process = MagicMock()  # Creating a mock process
    mock_process.poll.return_value = None  # Mocking process.poll to return None
    mock_process.pid = 1234  # Mocking process id
    mock_run.return_value = mock_process  # Mocking run_command to return mock process

    # When
    cli_response, llm_response, exit_code = execute_command(project, command, timeout, force=True)  # Calling execute_command with project, command, timeout, and force=True

    # Then
    assert cli_response is not None  # Asserting that cli_response is not None
    assert llm_response == 'DONE'  # Asserting that llm_response is 'DONE'
    assert exit_code is not None  # Asserting that exit_code is not None
    mock_terminate_process.assert_called_once_with(1234)  # Asserting that terminate_process was called once with process id 1234

def mock_run_command(command, path, q, q_stderr):  # Mock function for run_command
    q.put('hello')  # Putting 'hello' in queue
    mock_process = MagicMock()  # Creating a mock process
    mock_process.returncode = 0  # Mocking process return code to 0
    mock_process.pid = 1234  # Mocking process id to 1234
    return mock_process  # Returning mock process

@patch('helpers.cli.ask_user', return_value='')  # Patching ask_user to return an empty string
@patch('helpers.cli.run_command')  # Patching run_command function
@patch("helpers.cli.terminate_process")  # Patching terminate_process function
def test_execute_command_enter(mock_terminate_process, mock_run, mock_ask):  # Test function for execute_command when user enters a command
    # Given
    project = create_project()  # Creating a project
    command = 'echo hello'  # Command to be executed
    timeout = 1000  # Timeout value
    mock_run.side_effect = mock_run_command  # Mocking run_command with mock_run_command function

    # When
    cli_response, llm_response, exit_code = execute_command(project, command, timeout)  # Calling execute_command with project, command, and timeout

    # Then
    assert 'hello' in cli_response  # Asserting that 'hello' is in cli_response
    assert llm_response == 'DONE'  # Asserting that llm_response is 'DONE'
    assert exit_code == 0  # Asserting that exit_code is 0
    mock_terminate_process.assert_called_once_with(1234)  # Asserting that terminate_process was called once with process id 1234

@patch('helpers.cli.ask_user', return_value='yes')  # Patching ask_user to return 'yes'
@patch('helpers.cli.run_command')  # Patching run_command function
@patch("helpers.cli.terminate_process")  # Patching terminate_process function
def test_execute_command_yes(mock_terminate_process, mock_run, mock_ask):  # Test function for execute_command when user enters 'yes'
    # Given
    project = create_project()  # Creating a project
    command = 'echo hello'  # Command to be executed
    timeout = 1000  # Timeout value
    mock_run.side_effect = mock_run_command  # Mocking run_command with mock_run_command function

    # When
    cli_response, llm_response, exit_code = execute_command(project, command, timeout)  # Calling execute_command with project, command, and timeout

    # Then
    assert 'hello' in cli_response  # Asserting that 'hello' is in cli_response
    assert llm_response == 'DONE'  # Asserting that llm_response is 'DONE'
