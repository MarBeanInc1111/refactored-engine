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

# Initialize the tokenizer for counting tokens
tokenizer = tiktoken.get_encoding("cl100k_base")

def get_tokens_in_messages(messages: List[str]) -> int:
    """
    Calculate the total number of tokens in a list of messages.

    :param messages: List[str] - A list of messages, where each message is a string.
    :return: int - The total number of tokens in the messages.
    """

def test_api_access(project) -> bool:
    """
    Test the API access by sending a request to the API.

    :param project: The project object.
    :return: True if the request was successful, False otherwise.
    """

def create_gpt_chat_completion(messages: List[dict], req_type, project, function_calls: FunctionCallSet = None, prompt_data: dict = None, temperature: float = 0.7):
    """
    Call the LLM API to generate a chat completion.

    :param messages: List[dict] - A list of message dictionaries, where each message has a 'role' and 'content' key.
    :param req_type: str - The type of request.
    :param project: The project object.
    :param function_calls: (optional) FunctionCallSet - A set of function calls.
    :param prompt_data: (optional) dict - Prompt data.
    :param temperature: float - The temperature parameter for the LLM API.
    :return: dict - The response from the LLM API.
    """

def get_api_key_or_throw(env_key: str):
    """
    Get the API key from the environment variable or throw an exception.

    :param env_key: str - The name of the environment variable.
    :return: str - The API key.
    """

def stream_gpt_completion(data, req_type, project):
    """
    Stream the LLM API response and return the chat completion.

    :param data: dict - The data for the LLM API request.
    :param req_type: str - The type of request.
    :param project: The project object.
    :return: dict - The chat completion response.
    """
