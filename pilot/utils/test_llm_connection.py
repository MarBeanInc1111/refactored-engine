import builtins  # Import the built-in module
from json import JSONDecodeError  # Import JSONDecodeError from json module
import os  # Import the os module

# Import pytest and unittest.mock modules
import pytest
from unittest.mock import call, patch, Mock

# Import dotenv module
from dotenv import load_dotenv

# Import ValidationError from jsonschema module
from jsonschema import ValidationError

# Import custom modules
from const.function_calls import ARCHITECTURE, DEVELOPMENT_PLAN
from helpers.AgentConvo import AgentConvo
from helpers.Project import Project
from helpers.agents.Architect import Architect
from helpers.agents.TechLead import TechLead
from utils.function_calling import parse_agent_response, FunctionType
from test.test_utils import assert_non_empty_string
from test.mock_questionary import MockQuestionary
from utils.llm_connection import create_gpt_chat_completion, stream_gpt_completion, assert_json_response, assert_json_schema, clean_json_response, retry_on_exception
from main import get_custom_print

# Load environment variables from .env file
load_dotenv()

# Remove the "AUTOFIX_FILE_PATHS" variable from os.environ
os.environ.pop("AUTOFIX_FILE_PATHS", None)

def test_clean_json_response_True_False():
    # Given a JSON response with Title Case True and False
    response = '''
    ...
    '''

    # When
    response = clean_json_response(response)

    # Then the markdown is removed
    assert response.startswith('{')
    assert response.endswith('}')
    # And the booleans are converted to lowercase
    assert '"daemon":false,' in response
    assert '"boolean":false' in response
    assert '"another_True":true,' in response
    assert '"check_if_fixed":true' in response

def test_clean_json_response_boolean_in_python():
    # Given a JSON response with Python booleans in a content string
    response = '''
    ...
    '''

    # When
    response = clean_json_response(response)

    # Then the content string is left untouched
    assert '"content": "json = {\'is_true\': True,\n \'is_false\': False}"' in response

@patch('utils.llm_connection.styled_text', return_value='}')
class TestRetryOnException:
    def setup_method(self):
        self.function = {
            'name': 'test',
            'description': 'test schema',
            'parameters': {
                'type': 'object',
                'properties': {
                    'foo': {'type': 'string'},
                    'boolean': {'type': 'boolean'},
                    'items': {'type': 'array'}
                },
                'required': ['foo']
            }
        }

    def _create_wrapped_function(self, json_responses):
        project = Project({'app_id': 'test-app'})
        args = {}, 'test', project

        def retryable_assert_json_schema(data, _req_type, _project):
            json_string = json_responses.pop(0)
            if 'function_buffer' in data:
                json_string = data['function_buffer'] + json_string
            assert_json_schema(json_string, [self.function])
            return json_string

        return retry_on_exception(retryable_assert_json_schema), args

    def test_incomplete_value_string(self, mock_styled_text):
        # Given incomplete JSON
        wrapper, args = self._create_wrapped_function(['{"foo": "bar', '"}'])

        # When
        response = wrapper(*args)

        # Then should tell the LLM the JSON response is incomplete and to continue
        # 'Unterminated string starting at'
        assert response == '{"foo": "bar"}'
        assert 'function_error' not in args[0]
        # And the user should not need to be notified
        assert mock_styled_text.call_count == 0

    # ... (other test methods)
