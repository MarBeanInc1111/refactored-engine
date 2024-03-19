import pytest  # A library for writing tests for Python code
from unittest.mock import patch  # A library for creating mock objects

from helpers.AgentConvo import AgentConvo  # A class for managing agent-user conversations
from helpers.agents import Developer  # A class representing a developer agent
from .utils import create_project  # A function for creating a new project
from helpers.cli import terminate_running_processes  # A function for terminating running processes
from test.mock_questionary import MockQuestionary  # A class for creating a mock questionary object

@pytest.mark.ux_test  # A marker for identifying this test as a UX test
@patch('utils.questionary.get_saved_user_input')  # Mocking the get_saved_user_input function
@patch('helpers.cli.get_saved_command_run')  # Mocking the get_saved_command_run function
@patch('helpers.AgentConvo.get_saved_development_step')  # Mocking the get_saved_development_step function
@patch('helpers.AgentConvo.save_development_step')  # Mocking the save_development_step function
def test_continue_development(mock_4, mock_3, mock_2, mock_1):  # Function for testing the continue_development function
    # Given
    project = create_project('continue_development', 'hello_world_server')  # Creating a new project

    developer = Developer(project)  # Creating a new developer agent
    project.developer = developer  # Setting the project's developer to the new developer agent
    convo = AgentConvo(developer)  # Creating a new conversation with the developer agent
    convo.load_branch = lambda last_branch_name: None  # Setting the load_branch function to a lambda function that does nothing
    developer.run_command = 'node server.js'  # Setting the run_command attribute of the developer agent

    # Note: uncomment the following 2 lines and indent the remaining lines when debugging without console input
    mock_questionary = MockQuestionary(['r', 'continue'])  # Creating a mock questionary object
    with patch('utils.questionary.questionary', mock_questionary):  # Patching the questionary module with the mock questionary object

        # When
        # `continue_development` calls `run_command_until_success()` if the
