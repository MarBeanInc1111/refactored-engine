import json  # Importing json module for handling JSON data
import re  # Importing re module for regular expressions
from typing import Union, TypeVar, List, Dict, Literal, Optional, TypedDict, Callable  # Importing various types from typing module

JsonTypeBase = Union[str, int, float, bool, None, List["JsonType"], Dict[str, "JsonType"]]  # Define a type for JSON data
JsonType = TypeVar("JsonType", bound=JsonTypeBase)  # Define a type variable for JSON data

class FunctionParameters(TypedDict):
    """TypedDict class for function parameters"""
    type: Literal["object"]  # Literal type for the 'type' key, set to 'object'
    properties: dict[str, JsonType]  # Dictionary type for the 'properties' key
    required: Optional[list[str]]  # Optional list type for the 'required' key

class FunctionType(TypedDict):
    """TypedDict class for function type"""
    name: str  # String type for the 'name' key
    description: Optional[str]  # Optional string type for the 'description' key
    parameters: FunctionParameters  # FunctionParameters type for the 'parameters' key

class FunctionCall(TypedDict):
    """TypedDict class for function call"""
    name: str  # String type for the 'name' key
    parameters: str  # String type for the 'parameters' key

class FunctionCallSet(TypedDict):
    """TypedDict class for function call set"""
    definitions: list[FunctionType]  # List type of FunctionType for the 'definitions' key
    functions: dict[str, Callable]  # Dictionary type for the 'functions' key

def add_function_calls_to_request(gpt_data, function_calls: Union[FunctionCallSet, None]):
    """Function to add function calls to the request data"""
    # Check if function_calls is None and return None if true
    if function_calls is None:
        return None

    model: str = gpt_data['model']  # Assign the 'model' value from gpt_data to a variable 'model'
    is_instruct = 'llama' in model or 'anthropic' in model  # Define 'is_instruct' based on the value of 'model'

    gpt_data['functions'] = function_calls['definitions']  # Assign the 'definitions' value from function_calls to 'functions' key in gpt_data

    prompter = JsonPrompter(is_instruct)  # Create an instance of JsonPrompter class with 'is_instruct' as argument

    if len(function_calls['definitions']) > 1:
        function_call = None  # Set 'function_call' to None if the length of 'definitions' is greater than 1
    else:
        function_call = function_calls['definitions'][0]['name']  # Set 'function_call' to the 'name' value of the first item in 'definitions'

    function_call_message = {
        'role': 'user',  # Define the 'role' key with value 'user'
        'content': prompter.prompt('', function_calls['definitions'], function_call)  # Define the 'content' key with the result of prompter.prompt()
    }  # Create a dictionary with 'role' and 'content' keys

    gpt_data['messages'].append(function_call_message)  # Append the created dictionary to the 'messages' list in gpt_data

    return function_call_message  # Return the created dictionary

def parse_agent_response(response, function_calls: Union[FunctionCallSet, None]):
    """Function to parse the agent's response"""
    if function_calls:
        text = response['text']  # Assign the 'text' value from response to a variable 'text'
        return json.loads(text)  # Return the result of json.loads(text)

    return response['text']  # Return the 'text' value from response

class JsonPrompter:
    """JsonPrompter class for generating the prompt"""
    def __init__(self, is_instruct: bool = False):
        """Initialize the JsonPrompter class"""
        self.is_instruct = is_instruct  # Assign the 'is_instruct' argument to the 'is_instruct' attribute

    def function_descriptions(self, functions: list[FunctionType], function_to_call: str
    ) -> list[str]:
        """Function to get the descriptions of the functions"""
        return [
            f'# {function["name"]}: {function["description"]}'
            for function in functions
            if function["name"] == function_to_call and "description" in function
        ]

    def function_parameters(self, functions: list[FunctionType], function_to_call: str
    ) -> str:
        """Function to get the parameters of the function"""
        return next(json.dumps(function["parameters"]["properties"], indent=4) for function in functions if function["name"] == function_to_call)

    def function_data(self, functions: list[FunctionType], function_to_call: str
    ) -> str:
        """Function to get the data for the function"""
        return "\n".join(
            [
                "Here is the schema for the expected JSON object:",
                "```json",
                self.function_parameters(functions, function_to_call),
                "```",
            ]
        )

    def function_summary(self, function: FunctionType) -> str:
        """Function to get a summary of a function"""
        return f"- {function['name']}" + (f" - {function['description']}" if "description" in function else "")

    def functions_summary(self, functions: list[FunctionType]) -> str:
        """Function to get a summary of the functions"""
        return "Available functions:\n" + "\n".join(self.function_summary(function) for function in functions)

    def prompt(self, prompt: str, functions: list[FunctionType], function_to_call: Union[str, None] = None) -> str:
        """Function to generate the llama
