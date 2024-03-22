import json
import re
from typing import Any, Dict, List, Literal, Optional, TypeVar, Union
from typing_extensions import TypedDict

JsonTypeBase = Union[str, int, float, bool, None, List[JsonTypeBase], Dict[str, JsonTypeBase]]
JsonType = TypeVar("JsonType", bound=JsonTypeBase)


class FunctionParameters(TypedDict):
    type: Literal["object"]
    properties: Dict[str, JsonType]
    required: Optional[List[str]]


class FunctionType(TypedDict):
    name: str
    description: Optional[str]
    parameters: FunctionParameters


class FunctionCall(TypedDict):
    name: str
    parameters: str


class FunctionCallSet(TypedDict):
    definitions: List[FunctionType]
    functions: Dict[str, Any]


def add_function_calls_to_request(gpt_data: Dict[str, Any], function_calls: Optional[FunctionCallSet]) -> Optional[Dict[str, Any]]:
    """Add function calls to the request data."""
    if function_calls is None:
        return None

    model: str = gpt_data.get('model')
    is_instruct = 'llama' in model or 'anthropic' in model

    gpt_data['functions'] = function_calls['definitions']

    if is_instruct and function_calls['definitions']:
        first_function = function_calls['definitions'][0]
        function_call_message = {
            'role': 'function',
            'name': first_function['name'],
            'arguments': json.dumps(first_function['parameters']['properties']),
        }
        gpt_data['messages'].append(function_call_message)

    return function_call_message


def parse_agent_response(response: Dict[str, Any], function_calls: Optional[FunctionCallSet]) -> Any:
    """Parse the agent's response."""
    if function_calls:
        text = response.get('text')
        if text:
            return json.loads(text)

    return response.get('text')


class JsonPrompter:
    """JsonPrompter class for generating the prompt."""

    def __init__(self, is_instruct: bool = False):
        """Initialize the JsonPrompter class."""
        self.is_instruct = is_instruct

    def function_descriptions(self, functions: List[FunctionType], function_to_call: str) -> List[str]:
        """Get the descriptions of the functions."""
        return [
            f'# {function["name"]}: {function["description"]}'
            for function in functions
            if function["name"] == function_to_call and "description" in function
        ]

    def function_parameters(self, function: FunctionType) -> str:
        """Get the parameters of the function."""
        return json.dumps(function["parameters"]["properties"], indent=4)

    def function_data(self, function: FunctionType) -> str:
        """Get the data for the function."""
        return "\n".join(
            [
                "Here is the schema for the expected JSON object:",
                "```json",
                self.function_parameters(function),
                "```",
            ]
        )

    def function_summary(self, function: FunctionType) -> str:
        """Get a summary of a function."""
        return f"- {function['name']}" + (f" - {function['description']}" if "description" in function else "")

    def functions_summary(self, functions: List[FunctionType]) -> str:
        """Get a summary of the functions."""
        return "Available functions:\n" + "\n".join(self.function_summary(function) for function in functions)

    def prompt(self, prompt: str, functions: List[FunctionType], function_to_call: Optional[str] = None) -> str:
        """Generate the prompt."""
        if self.is_instruct:
            if function_to_call:
                descriptions = self.function_descriptions(functions, function_to_call)
                if descriptions:
                    prompt += "\n\n" + "\n".join(descriptions)

                parameters = self.function_parameters(functions[0])
                if parameters:
                    prompt += "\n\n" + self.function_data(functions[0])

        return prompt


if __name__ == "__main__":
    # Example usage of the functions and classes
    pass
