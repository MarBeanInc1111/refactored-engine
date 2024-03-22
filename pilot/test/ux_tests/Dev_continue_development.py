import pytest
from unittest.mock import patch
from helpers.AgentConvo import AgentConvo
from helpers.agents import Developer
from helpers.cli import terminate_running_processes
from helpers.projects import Project
from test.mock_questionary import MockQuestionary

@pytest.mark.ux_test
@patch('utils.questionary.get_saved_user_input')
@patch('helpers.cli.get_saved_command_run')
@patch('helpers.AgentConvo.get_saved_development_step')
@patch('helpers.AgentConvo.save_development_step')
def test_continue_development(mock_save_development_step, mock_get_saved_development_step, mock_get_saved_command_run, mock_get_saved_user_input):
    # Arrange
    project_name = 'continue_development'
    app_name = 'hello_world_server'
    project = Project.create(project_name, app_name)

    developer = Developer(project)
    project.developer = developer
    convo = AgentConvo(developer)
    convo.load_branch = lambda last_branch_name: None
    developer.run_command = 'node server.js'

    mock_questionary = MockQuestionary(['r', 'continue'])
    with patch('utils.questionary.questionary', mock_questionary):
        # Act
        convo.continue_development()

        # Assert
        mock_get_saved_development_step.assert_called_once()
        mock_get_saved_command_run.assert_called_once()
        mock_save_development_step.assert_called_once()
        terminate_running_processes.assert_called_once_with(developer.run_command)
