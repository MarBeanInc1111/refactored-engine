import builtins # Importing the built-in module
import json # Importing the json module

import pytest # Importing the pytest module
from unittest.mock import patch, MagicMock # Importing patch and MagicMock from unittest.mock
from dotenv import load_dotenv # Importing load_dotenv from dotenv

load_dotenv() # Loading environment variables from .env file

from utils.custom_print import get_custom_print # Importing get_custom_print from custom_print module
from helpers.agents.Developer import Developer # Importing Developer class from Developer module
from helpers.AgentConvo import AgentConvo # Importing AgentConvo class from AgentConvo module
from helpers.Debugger import Debugger # Importing Debugger class from Debugger module
from helpers.test_Project import create_project # Importing create_project from test_Project module
from test.mock_questionary import MockQuestionary # Importing MockQuestionary from mock_questionary module

################## NOTE: this test needs to be ran in debug with breakpoints ##################

@pytest.mark.uses_tokens # Decorator to indicate that this test uses tokens
@patch('pilot.helpers.AgentConvo.get_saved_development_step') # Patching get_saved_development_step
@patch('pilot.helpers.AgentConvo.save_development_step') # Patching save_development_step
@patch('utils.questionary.save_user_input') # Patching save_user_input
@patch('helpers.cli.run_command') # Patching run_command
@patch('helpers.cli.save_command_run') # Patching save_command_run
# @patch('pilot.helpers.cli.execute_command', return_value=('', 'DONE', 0')) # Patching execute_command
def test_debug( # Defining test_debug function
        # mock_execute_command, # Mock object for execute_command
        mock_save_command, mock_run_command, # Mock objects for save_command and run_command
        mock_save_input, mock_save_step, mock_get_saved_step): # Mock objects for save_input, save_step and get_saved_step

    # Given
    builtins.print, ipc_client_instance = get_custom_print({}) # Calling get_custom_print function
    project = create_project() # Creating a new project
    project.current_step = 'coding' # Setting current_step to 'coding'
    developer = Developer(project) # Creating a new Developer instance
    project.developer = developer # Setting developer of the project
    convo = AgentConvo(developer) # Creating a new AgentConvo instance
    convo.load_branch = lambda x: None # Setting load_branch to a lambda function

    debugger = Debugger(developer) # Creating a new Debugger instance

    # convo.messages.append() # Adding a message to convo.messages
    convo.construct_and_add_message_from_prompt('dev_ops/ran_command.prompt', { # Constructing and adding a message from a prompt
        'cli_response': ''' # cli_response content
stderr:


stdout:


''' # cli_response content end
    })

    mock_questionary = MockQuestionary(['', ''])\

    with patch('utils.questionary.questionary', mock_questionary):
        # When
        result = debugger.debug(convo, command={'command': 'npm run start'}, is_root_task=True)\

        # Then
        assert result == {'success': True}\

@patch('helpers.AgentConvo.create_gpt_chat_completion') # Patching create_gpt_chat_completion
@patch('helpers.AgentConvo.save_development_step') # Patching save_development_step
def test_debug_need_to_see_output(mock_save_step, mock_get_completion): # Defining test_debug_need_to_see_output function
    # Given
    builtins.print, ipc_client_instance = get_custom_print({}) # Calling get_custom_print function
    project = create_project() # Creating a new project
    project.current_step = 'coding' # Setting current_step to 'coding'
    developer = Developer(project
