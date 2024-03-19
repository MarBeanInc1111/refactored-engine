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
    def setup_method(self):
        # Setting up the method for each test
        builtins.print, ipc_client_instance = get_custom_print({})  # Getting custom print function

        name = 'TestDeveloper'  # Defining name
        self.project = create_project()  # Creating project
        self.project.app_id = 'test-developer'  # Setting app_id
        self.project.name = name  # Setting name
        self.project.set_root_path(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                              '../../../workspace/TestDeveloper')))  # Setting root path

        self.project.technologies = []  # Initializing technologies as empty list
        self.project.current_step = ENVIRONMENT_SETUP_STEP  # Setting current_step
        self.developer = Developer(self.project)  # Creating developer object

    @pytest.mark.uses_tokens  # Using pytest mark for uses_tokens
    @patch('helpers.AgentConvo.save_development_step')  # Patching save_development_step
    @patch('helpers.AgentConvo.create_gpt_chat_completion', return_value={'text': '{"command": "python --version", "timeout": 10}'})  # Patching create_gpt_chat_completion
    @patch('helpers.cli.execute_command', return_value=('', 'DONE', None))  # Patching execute_command
    def test_install_technology(self, mock_execute_command, mock_completion, mock_save):
        # Test function for install_technology
        self.developer.convo_os_specific_tech = AgentConvo(self.developer)  # Creating convo_os_specific_tech

        # Calling install_technology and storing the result in llm_response
        llm_response = self.developer.check_system_dependency('python')

        # Asserting that llm_response is equal to 'DONE'
        assert llm_response == 'DONE'

        # Asserting that execute_command was called once with the correct arguments
        mock_execute_command.assert_called_once_with(self.project, 'python --version', timeout=10, command_id=None)


    def test_implement_task(self, mock_completion, mock_save):
        # Test function for implement_task
        project = create_project()  # Creating project
        project.project_description = 'Test Project'  # Setting project_description
        project.development_plan = [{'description': 'Do stuff', 'user_review_goal': 'Do stuff'}]  # Setting development_plan
        project.get_all_coded_files = lambda: []  # Setting get_all_coded_files
        project.current_step = 'test'  # Setting current_step

        developer = Developer(project)  # Creating developer object
        developer.execute_task = MagicMock()  # Creating execute_task MagicMock
        developer.execute_task.return_value = {'success': True}  # Setting return value of execute_task

        # Calling implement_task and storing the result in developer.execute_task.call_args
        developer.implement_task(0, 'test', {'description': 'Do stuff'})

        # Asserting that execute_task was called once with the correct arguments
        assert developer.execute_task.call_count == 1
        assert developer.execute_task.call_args[0][1] == [{'command': 'ls -al'}]


    def test_implement_task_reject_with_user_input(self, mock_completion, mock_save):
        # Test function for implement_task_reject_with_user_input
        project = create_project()  # Creating project
        project.project_description = 'Test Project'  # Setting project_description
        project.development_plan = [{'description': 'Do stuff', 'user_review_goal': 'Do stuff'}]  # Setting development_plan
        project.get_all_coded_files = lambda: []  # Setting get_all_coded_files
        project.current_step = 'test'  # Setting current_step

        developer = Developer(project)  # Creating developer object
        developer.execute_task = MagicMock()  # Creating execute_task MagicMock

        # Setting side effect for execute_task
        developer.execute_task.side_effect = [{'success': False, 'step_index': 2, 'user_input': 'no, use a better command'}, {'success': True}]

        # Calling implement_task and storing the result in developer.execute_task.call_args
        developer.implement_task(0, 'test', {'description': 'Do stuff'})

        # Asserting that execute_task was called twice with the
