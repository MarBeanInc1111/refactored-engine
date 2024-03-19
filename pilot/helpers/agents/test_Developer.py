import builtins  # Importing builtins module
import json  # Importing json module
import os  # Importing os module
import pytest  # Importing pytest module
from unittest.mock import patch, MagicMock  # Importing patch and MagicMock from unittest.mock

import requests  # Importing requests module

from helpers.AgentConvo import AgentConvo  # Importing AgentConvo from helpers
from dotenv import load_dotenv  # Importing load_dotenv from dotenv
load_dotenv()  # Loading environment variables from .env file

from main import get_custom_print  # Importing get_custom_print from main
from .Developer import Developer, ENVIRONMENT_SETUP_STEP  # Importing Developer and ENVIRONMENT_SETUP_STEP from Developer
from test.mock_questionary import MockQuestionary  # Importing MockQuestionary from test
from helpers.test_Project import create_project  # Importing create_project from helpers

class TestDeveloper:
    @pytest.fixture(scope='function')
    def setup_developer(self):
        # Setting up the method for each test
        builtins.print, ipc_client_instance = get_custom_print({})  # Getting custom print function

        name = 'TestDeveloper'  # Defining name
        project = create_project()  # Creating project
        project.app_id = 'test-developer'  # Setting app_id
        project.name = name  # Setting name
        project.set_root_path(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                              '../../../workspace/TestDeveloper')))  # Setting root path

        project.technologies = []  # Initializing technologies as empty list
        project.current_step = ENVIRONMENT_SETUP_STEP  # Setting current_step
        developer = Developer(project)  # Creating developer object

        developer.convo_os_specific_tech = AgentConvo(developer)  # Creating convo_os_specific_tech

        yield developer  # Yielding the developer object for use in the test

        # Cleaning up after the test
        del developer

    @pytest.mark.uses_tokens  # Using pytest mark for uses_tokens
    @patch('helpers.AgentConvo.save_development_step')  # Patching save_development_step
    @patch('helpers.AgentConvo.create_gpt_chat_completion', return_value={'text': '{"command": "python --version", "timeout": 10}'})  # Patching create_gpt_chat_completion
    @patch('helpers.cli.execute_command', return_value=('', 'DONE', None))  # Patching execute_command
    def test_install_technology(self, mock_execute_command, mock_completion, mock_save, setup_developer):  # Adding setup_developer fixture
        # Test function for install_technology
        developer = setup_developer  # Getting the developer object from the fixture

        # Calling install_technology and storing the result in llm_response
        llm_response = developer.check_system_dependency('python')

        # Asserting that llm_response is equal to 'DONE'
        assert llm_response == 'DONE'

        # Asserting that execute_command was called once with the correct arguments
        mock_execute_command.assert_called_once_with(developer.project, 'python --version', timeout=10, command_id=None)


    @patch('helpers.AgentConvo.create_gpt_chat_completion', return_value={'text': '{"command": "ls -al", "timeout": 10}'})  # Patching create_gpt_chat_completion
    @patch('helpers.cli.execute_command', return_value=('', 'DONE', None))  # Patching execute_command
    def test_implement_task(self, mock_execute_command, mock_completion, setup_developer):  # Adding setup_developer fixture
        # Test function for implement_task
        developer = setup_developer  # Getting the developer object from the fixture
        developer.execute_task = MagicMock()  # Creating execute_task MagicMock
        developer.execute_task.return_value = {'success': True}  # Setting return value of execute_task

        # Calling implement_task and storing the result in developer.execute_task.call_args
        developer.implement_task(0, 'test', {'description': 'Do stuff'})

        # Asserting that execute_task was called once with the correct arguments
        assert developer.execute_task.call_count == 1
        assert developer.execute_task.call_args[0][1] == [{'command': 'ls -al'}]


    @patch('helpers.AgentConvo.create_gpt_chat_completion', side_effect=[{'text': '{"command": "ls -al", "timeout": 10}', 'error': None},
                                                                         {'text': '{"command": "echo hello", "timeout": 10}', 'error': None}])  # Patching create_gpt_chat_completion
    @patch('helpers.cli.execute_command', return_value=('', 'DONE', None))  # Patching execute_command
    def test_implement_task_reject_with_user_input(self, mock_execute_command, mock_completion, setup_developer):  # Adding setup_developer fixture
        # Test function for implement_task_reject_with_user_input
        developer = setup_developer  # Getting the developer object from the fixture
        developer.execute_task = MagicMock()  # Creating execute_task MagicMock

        # Calling implement_task and storing the result in developer.execute_task.call_args
        developer.implement_task(0, 'test', {'description': 'Do stuff'})

        # Asserting that execute_task was called twice with the correct arguments
        assert developer.execute_
