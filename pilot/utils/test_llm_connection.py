import builtins
from json import JSONDecodeError
import os

import pytest
from unittest.mock import call, patch, Mock
from jsonschema import ValidationError, Draft7Validator
from dotenv import load_dotenv

from const.function_calls import ARCHITECTURE, DEVELOPMENT_PLAN
from helpers.AgentConvo import AgentConvo
from helpers.Project import Project
from helpers.agents.Architect import Architect
from helpers.agents.TechLead import TechLead
from utils.function_calling import parse_agent_response, FunctionType
from test.test_utils import assert_non_empty_string
from test.mock_questionary import MockQuestionary
from utils.llm_connection import create_gpt_chat_completion, stream_gpt_completion, assert_json_response, assert_json_schema, clean_json_response, retry_on_exception

load_dotenv()
os.environ.pop("AUTOFIX_FILE_PATHS", None)


def test_clean_json_response_true_false():
    """Test cleaning JSON response with Title Case True and False."""
    response = '''
    ...
    '''

    response = clean_json_response(response)

    assert response.startswith('{')
    assert response.endswith('}')
    assert '"daemon":false,' in response
    assert '"boolean":false' in response
    assert '"another_True":true,' in response
    assert '"check_if_fixed":true' in response


def test_clean_json_response_boolean_in_python():
    """Test cleaning JSON response with Python booleans in a content string."""
    response = '''
    ...
    '''

    response = clean_json_response(response)

    assert '"content": "json = {\'is_true\': True,\n \'is_false\': False}"' in response


@pytest.mark.parametrize(
    "json_responses,expected_response",
    [
        (['{"foo": "bar", "boolean": false, "items": [1, 2, 3]}'], '{"foo": "bar", "boolean": false, "items": [1, 2, 3]}'),
        (['{"foo": "bar", "boolean": true, "items": [1, 2, 3]}'], '{"foo": "bar", "boolean": true, "items": [1, 2, 3]}'),
        (['{"foo": "bar", "boolean": "false", "items": [1, 2, 3]}'], '{"foo": "bar", "boolean": "false", "items": [1, 2, 3]}'),
        (['{"foo": "bar", "boolean": "true", "items": [1, 2, 3]}'], '{"foo": "bar", "boolean": "true", "items": [1, 2, 3]}'),
    ],
)
def test_clean_json_response_boolean_validation(json_responses, expected_response):
    """Test cleaning JSON response with different boolean values."""
    wrapper, args = _create_wrapped_function(json_responses)
    response = wrapper(*args)
    assert response == expected_response


def _create_wrapped_function(json_responses):
    project = Project({'app_id': 'test-app'})
    args = {}, "test", project

    def retryable_assert_json_schema(data, _req_type, _project):
        json_string = json_responses.pop(0)
        if 'function_buffer' in data:
            json_string = data['function_buffer'] + json_string
        assert_json_schema(json_string, [{"type": "object", "properties": {"foo": {"type": "string"}}, "required": ["foo"]}])
        return json_string

    return retry_on_exception(retryable_assert_json_schema), args


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
            Draft7Validator.check_schema(self.function)
            assert_json_schema(json_string, [self.function])
            return json_string

        return retry_on_exception(retryable_assert_json_schema), args

    def test_incomplete_value_string(self, mock_styled_text):
        """Test retry_on_exception with incomplete JSON."""
        wrapper, args = self._create_wrapped_function(['{"foo": "bar', '"}'])

        with pytest.raises(ValueError):
            wrapper(*args)

        # Then should tell the LLM the JSON response is incomplete and to continue
        # 'Unterminated string
