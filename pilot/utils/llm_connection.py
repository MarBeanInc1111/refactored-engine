import re
import requests
import os
import sys
import time
import json
import tiktoken
from prompt_toolkit.styles import Style

from jsonschema import validate, ValidationError
from utils.style import color_red, color_yellow
from typing import List
from const.llm import MAX_GPT_MODEL_TOKENS, API_CONNECT_TIMEOUT, API_READ_TIMEOUT
from const.messages import AFFIRMATIVE_ANSWERS
from logger.logger import logger, logging
from helpers.exceptions import TokenLimitError, ApiKeyNotDefinedError, ApiError
from utils.utils import fix_json, get_prompt
from utils.function_calling import add_function_calls_to_request, FunctionCallSet, FunctionType
from utils.questionary import styled_text

from .telemetry import telemetry

tokenizer = tiktoken.get_encoding("cl100k_base")


def get_tokens_in_messages(messages: List[str]) -> int:
    tokenized_messages = [tokenizer.encode(message['content']) for message in messages]
    return sum(len(tokens) for tokens in tokenized_messages)


def test_api_access(project) -> bool:
    """
    Test the API access by sending a request to the API.

    :returns: True if the request was successful, False otherwise.
    """
    messages = [
        {
            "role": "user",
            "content": "This is a connection test. If you can see this, please respond only with 'START' and nothing else."
        }
    ]

    endpoint = os.getenv('ENDPOINT')
    model = os.getenv('MODEL_NAME', 'gpt-4')
    try:
        response = create_gpt_chat_completion(messages, 'project_description', project)
        if response is None or response == {}:
            print(color_red("Error connecting to the API. Please check your API key/endpoint and try again."))
            logger.error(f"The request to {endpoint} model {model} API failed.")
            return False
        return True
    except Exception as err:
        print(color_red("Error connecting to the API. Please check your API key/endpoint and try again."))
        logger.error(f"The request to {endpoint} model {model} API failed: {err}", exc_info=err)
        return False


def create_gpt_chat_completion(messages: List[dict], req_type, project,
                               function_calls: FunctionCallSet = None,
                               prompt_data: dict = None,
                               temperature: float = 0.7):
    """
    Called from:
      - AgentConvo.send_message() - these calls often have `function_calls`, usually from `pilot/const/function_calls.py`
         - convo.continuous_conversation()
    :param messages: [{ "role": "system"|"assistant"|"user", "content": string }, ... ]
    :param req_type: 'project_description' etc. See common.STEPS
    :param project: project
    :param function_calls: (optional) {'definitions': [{ 'name': str }, ...]}
        see `IMPLEMENT_CHANGES` etc. in `pilot/const/function_calls.py`
    :param prompt_data: (optional) { 'prompt': str, 'variables': { 'variable_name': 'variable_value', ... } }
    :return: {'text': new_code}
        or if `function_calls` param provided
             {'function_calls': {'name': str, arguments: {...}}}
    """

    gpt_data = {
        'model': os.getenv('MODEL_NAME', 'gpt-4'),
        'n': 1,
        'temperature': temperature,
        'top_p': 1,
        'presence_penalty': 0,
        'frequency_penalty': 0,
        'messages': messages,
        'stream': True
    }

    # delete some keys if using "OpenRouter" API
    if os.getenv('ENDPOINT') == 'OPENROUTER':
        keys_to_delete = ['n', 'max_tokens', 'temperature', 'top_p', 'presence_penalty', 'frequency_penalty']
        for key in keys_to_delete:
            if key in gpt_data:
                del gpt_data[key]

    # Advise the LLM of the JSON response schema we are expecting
    messages_length = len(messages)
    function_call_message = add_function_calls_to_request(gpt_data, function_calls)
    if prompt_data is not None and function_call_message is not None:
        prompt_data['function_call_message'] = function_call_message

    try:
        response = stream_gpt_completion(gpt_data, req_type, project)

        # Remove JSON schema and any added retry messages
        while len(messages) > messages_length:
            messages.pop()
        return response
    except TokenLimitError as e:
        raise e
    except Exception as e:
        logger.error(f'The request to {os.getenv("ENDPOINT")} API failed: %s', e)
        print(color_red(f'The request to {os.getenv("ENDPOINT")} API failed with error: {e}. Please try again later.'))
        if isinstance(e, ApiError):
            raise e
        else:
            raise ApiError(f"Error making LLM API request: {e}") from e


def get_api_key_or_throw(env_key: str):
    api_key = os.getenv(env_key)
    if api_key is None:
        raise ApiKeyNotDefinedError(env_key)
    return api_key


def stream_gpt_completion(data, req_type, project):
    """
    Called from create_gpt_chat_completion()
    :param data:
    :param req_type: 'project_description' etc. See common.STEPS
    :param project: NEEDED FOR WRAPPER FUNCTION retry_on_exception
    :return: {'text': str} or {'function_calls': {'name': str, arguments: '{...}'}}
    """
    # Configure for the selected ENDPOINT
    model = os.getenv('MODEL_NAME', 'gpt-4')
    endpoint = os.getenv('ENDPOINT')

    logger.info(f'> Request model: {model}')
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug('\n'.join([f"{message['role']}: {message['content']}" for message in data['messages']]))

    if endpoint == 'AZURE':
        # If yes, get the AZURE_ENDPOINT from .ENV file
        endpoint_url = os.getenv('AZURE_ENDPOINT') + '/openai/deployments/' + model + '/chat/completions?api-version=2023-05-15'
        headers = {
            'Content-Type': 'application/json',
            'api-key': get_api_key_or_throw('AZURE_API_KEY')
        }
    elif endpoint == 'OPENROUTER':
        # If so, send the request to the OpenRouter API endpoint
        endpoint_url = os.getenv('OPENROUTER_ENDPOINT', 'https://openrouter.ai/api/v1/chat/completions')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + get_api_key_or_throw('OPENROUTER_API_KEY'),
            'HTTP-Referer': 'https://github.com/Pythagora-io/gpt-pilot',
            'X-Title': 'GPT Pilot'
        }
        data['max_tokens'] = MAX_GPT_MODEL_TOKENS
        data['model'] = model
    else:
        # If not, send the request to the OpenAI endpoint
        endpoint_url = os.getenv('OPENAI_ENDPOINT', 'https://api.openai.com/v1/chat/completions')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + get_api_key_or_throw('OPENAI_API_KEY')
        }
        data['model'] = model

    telemetry.set("model", model)
    token_count = get_tokens_in_messages(data['messages'])
    request_start_time = time.time()

    response = requests.post(
        endpoint_url,
        headers=headers,
        json=data,
        stream=True,
        timeout=(API_CONNECT_TIMEOUT, API_READ_TIMEOUT),
    )

    if response.status_code == 401 and 'BricksLLM' in response.text:
        print("", type='keyExpired')
        msg = "Trial Expired"
        key = os.getenv("OPENAI_API_KEY")
        endpoint = os.getenv("OPENAI_ENDPOINT")
        if key:
            msg += f"\n\n(using key ending in ...{key[-4:]}):"
        if endpoint:
            msg += f"\n(using endpoint: {endpoint}):"
        msg += f"\n\nError details: {response.text}"
        raise ApiError(msg, response=response)

    if response.status_code != 200:
        project.dot_pilot_gpt.log_chat_completion(endpoint, model, req_type, data['messages'], response.text)
        logger.info(f'problem with request (status {response.status_code}): {response.text}')
        telemetry.record_llm_request(token_count, time.time() - request_start_time, is_error=True)
        raise ApiError(f"API responded with status code: {response.status_code}. Request token size: {token_count} tokens. Response text: {response.text}", response=response)

    gpt_response = ''
    for line in response.iter_lines():
        # Ignore keep-alive new lines
        if line and line != b': OPENROUTER PROCESSING':
            line = line.decode("utf-8")  # decode the bytes to string

            if line.startswith('data: '):
                line = line[6:]  # remove the 'data: ' prefix

            # Check if the line is "[DONE]" before trying to parse it as JSON
            if line == "[DONE]":
                continue

            try:
                json_line = json.loads(line)

                if len(json_line['choices']) == 0:
                    continue

                if 'error' in json_line:
                    logger.error(f'Error in LLM response: {json_line}')
                    telemetry.record_llm_request(token_count, time.time() - request_start_time, is_error=True)
                    raise ValueError(f'Error in LLM response: {json_line["error"]["message"]}')

                choice = json_line['choices'][0]
                json_line = choice['delta']

            except json.JSONDecodeError as e:
                logger.error(f'Unable to decode line: {line} {e.msg}')
                continue  # skip to the next line

            if 'content' in json_line:
                content = json_line.get('content')
                if content:
                    gpt_response += content

    telemetry.record_llm_request(
        token_count + len(tokenizer.encode(gpt_response)),
        time.time() - request_start_time,
        is_error=False
    )

    logger.info('<<<<<<<<<< LLM Response <<<<<<<<<<\n%s\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<', gpt_response)
    project.dot_pilot_gpt.log_chat_completion(endpoint, model, req_type, data['messages'], gpt_response)

    return {'text': gpt_response}