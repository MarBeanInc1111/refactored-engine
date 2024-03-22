import builtins
import json
import os
import pytest
from unittest.mock import patch, MagicMock
import requests
from helpers.AgentConvo import AgentConvo
from dotenv import load_dotenv
from main import get_custom_print
from .Developer import Developer, ENVIRONMENT_SETUP_STEP
from test.mock_questionary import MockQuestionary
from helpers.test_Project import create_project

class TestDeveloper:
    @pytest.fixture(scope='function')
    def setup_developer(self):
        builtins.print = get_custom_print({})[0]

        name = 'TestDeveloper'
        project = create_project()
        project.app_id = 'test-developer'
        project.name = name
        project.set_root_path(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../workspace/TestDeveloper')))

        project.technologies = []
        project.current_step = ENVIRONMENT_SETUP_STEP
        developer = Developer(project)

        developer.convo_os_specific_tech = AgentConvo(developer)

        yield developer

    @pytest.mark.uses_tokens
    @patch('helpers.AgentConvo.save_development_step')
    @patch('helpers.AgentConvo.create_gpt_chat_completion', return_value={'text': '{"command": "python --version", "timeout": 10}'})
    @patch('helpers.cli.execute_command', return_value=('', 'DONE', None))
    def test_install_technology(self, mock_execute_command, mock_completion, mock_save, setup_developer):
        developer = setup_developer

        llm_response = developer.check_system_dependency('python')

        assert llm_response == 'DONE'
        mock_execute_command.assert_called_once_with(developer.project, 'python --version', timeout=10, command_id=None)

    @patch('helpers.AgentConvo.create_gpt_chat_completion', return_value={'text': '{"command": "ls -al", "timeout": 10}'})
    @patch('helpers.cli.execute_command', return_value=('', 'DONE', None))
    def test_implement_task(self, mock_execute_command, mock_completion, setup_developer):
        developer = setup_developer
        developer.execute_task = MagicMock()
        developer.execute_task.return_value = {'success': True}

        developer.implement_task(0, 'test', {'description': 'Do stuff'})

        assert developer.execute_task.call_count == 1
        assert developer.execute_task.call_args[0][1] == [{'command': 'ls -al'}]

    @patch('helpers.AgentConvo.create_gpt_chat_completion', side_effect=[{'text': '{"command": "ls -al", "timeout": 10}', 'error': None},
                                                                         {'text': '{"command": "echo hello", "timeout": 10}', 'error': None}])
    @patch('helpers.cli.execute_command', return_value=('', 'DONE', None))
    def test_implement_task_reject_with_user_input(self, mock_execute_command, mock_completion, setup_developer):
        developer = setup_developer
        developer.execute_task = MagicMock()

        developer.implement_task(0, 'test', {'description': 'Do stuff'})

        assert developer.execute_task.call_count == 2
        assert developer.execute_task.call_args_list[0][0][1] == [{'command': 'ls -al'}]
        assert developer.execute_task.call_args_list[1][0][1] == [{'command': 'echo hello'}]
