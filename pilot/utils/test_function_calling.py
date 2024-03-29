from const.function_calls import ARCHITECTURE, USER_TASKS
from utils.llm_connection import clean_json_response
from .function_calling import parse_agent_response, JsonPrompter

class TestFunctionCalling:
    def test_parse_agent_response_text(self):
        response = {'text': 'Hello world!'}
        response = parse_agent_response(response, None)
        assert response == 'Hello world!'

    def test_parse_agent_response_json(self):
        response = {'text': '{"greeting": "Hello world!"}'}
        function_calls = {'definitions': [], 'functions': {}}
        response = parse_agent_response(response, function_calls)
        assert response == {'greeting': 'Hello world!'}

    def test_parse_agent_response_json_markdown(self):
        response = {'text': '```json\n{"greeting": "Hello world!"}\n```'}
        function_calls = {'definitions': [], 'functions': {}}
        response['text'] = clean_json_response(response['text'])
        response = parse_agent_response(response, function_calls)
        assert response == {'greeting': 'Hello world!'}

    def test_parse_agent_response_markdown(self):
        response = {'text': '```\n{"greeting": "Hello world!"}\n```'}
        function_calls = {'definitions': [], 'functions': {}}
        response['text'] = clean_json_response(response['text'])
        response = parse_agent_response(response, function_calls)
        assert response == {'greeting': 'Hello world!'}

    def test_parse_agent_response_multiple_args(self):
        response = {'text': '{"greeting": "Hello", "name": "John"}'}
        function_calls = {'definitions': [], 'functions': {}}
        response = parse_agent_response(response, function_calls)
        assert response['greeting'] == 'Hello'
        assert response['name'] == 'John'

def test_json_prompter():
    prompter = JsonPrompter()
    prompt = prompter.prompt('Create a web-based chat app', ARCHITECTURE['definitions'])
    expected_prompt = '''Help choose the appropriate function to call to answer the user's question.
You must respond with ONLY the JSON object, with NO additional text or explanation.

Available functions:\n- process_architecture - Get architecture and the list of system dependencies required for the project.'''
    assert prompt == expected_prompt

def test_llama_json_prompter():
    prompter = JsonPrompter(is_instruct=True)
    prompt = prompter.prompt('Create a web-based chat app', ARCHITECTURE['definitions'])
    expected_prompt = '''[INST] Help choose the appropriate function to call to answer the user's question.
You must respond with ONLY the JSON object, with NO additional text or explanation.

Available functions:\n- process_architecture - Get architecture and the list of system dependencies required for the project.<</SYS>»

Create a web-based chat app'''
    assert prompt == expected_prompt

def test_json_prompter_named():
    prompter = JsonPrompter()
    prompt = prompter.prompt('Create a web-based chat app', USER_TASKS['definitions'], 'process_user_tasks')
    expected_prompt = '''**IMPORTANT**\nYou must respond with ONLY the JSON object, with NO additional text or explanation.\n\nHere is the schema for the expected JSON object:\n\n\nCreate a web-based chat app'''
    assert prompt == expected_prompt
