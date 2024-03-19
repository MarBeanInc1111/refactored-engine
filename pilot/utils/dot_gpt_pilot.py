import json  # Importing json module for handling JSON data.
import os  # Importing os module for handling file system operations.
import yaml  # Importing yaml module for handling YAML data.
from datetime import datetime  # Importing datetime module for getting current date and time.
from dotenv import load_dotenv  # Importing dotenv module for loading environment variables from .env file.

# Load environment variables from .env file.
load_dotenv()

# Global variable to check if the '.gpt-pilot' directory should be used.
USE_GPTPILOT_FOLDER = os.getenv('USE_GPTPILOT_FOLDER') == 'true'

class DotGptPilot:
    """
    Manages the '.gpt-pilot' directory.
    """

    def __init__(self, log_chat_completions: bool = True):
        """
        Initialize the DotGptPilot class.

        :param log_chat_completions: Boolean flag to enable or disable logging of chat completions. Defaults to True.
        """
        if not USE_GPTPILOT_FOLDER:
            return

        self.log_chat_completions = log_chat_completions
        self.dot_gpt_pilot_path = self.with_root_path('~', create=False)
        self.chat_log_path = self.chat_log_folder(None)

    def with_root_path(self, root_path: str, create=True):
        """
        Get or create the '.gpt-pilot' directory with the given root path.

        :param root_path: Root path for the '.gpt-pilot' directory.
        :param create: Boolean flag to enable or disable creating the directory. Defaults to True.
        :return: The absolute path of the '.gpt-pilot' directory.
        """
        if not USE_GPTPILOT_FOLDER:
            return

        dot_gpt_pilot_path = os.path.expanduser(os.path.join(root_path, '.gpt-pilot'))
        self.dot_gpt_pilot_path = dot_gpt_pilot_path

        if create and self.log_chat_completions:
            self.chat_log_folder(None)

        return dot_gpt_pilot_path

    def chat_log_folder(self, task):
        """
        Get or create the chat log folder in the '.gpt-pilot' directory.

        :param task: Task number for the chat log folder. If None, the root chat log folder is returned.
        :return: The absolute path of the chat log folder.
        """
        if not USE_GPTPILOT_FOLDER:
            return

        chat_log_path = os.path.join(self.dot_gpt_pilot_path, 'chat_log')
        if task is not None:
            chat_log_path = os.path.join(chat_log_path, 'task_' + str(task))

        os.makedirs(chat_log_path, exist_ok=True)
        self.chat_log_path = chat_log_path
        return chat_log_path

    def log_chat_completion(self, endpoint, model, req_type, messages, response):
        """
        Log a chat completion in the chat log folder.

        :param endpoint: Endpoint for the chat completion.
        :param model: Model used for the chat completion.
        :param req_type: Type of request for the chat completion.
        :param messages: List of messages for the chat completion.
        :param response: Response from the chat completion.
        """
        if not USE_GPTPILOT_FOLDER:
            return

        if self.log_chat_completions:
            time = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            with open(os.path.join(self.chat_log_path, f'{time}-{req_type}.yaml'), 'w', encoding="utf-8") as file:
                data = {
                    'endpoint': endpoint,
                    'model': model,
                    'messages': messages,
                    'response': response,
                }

                yaml.safe_dump(data, file, width=120, indent=2, default_flow_style=False, sort_keys=False)

    def log_chat_completion_json(self, endpoint, model, req_type, functions, json_response):
        """
        Log a chat completion in the chat log folder in JSON format.

        :param endpoint: Endpoint for the chat completion.
        :param model: Model used for the chat completion.
        :param req_type: Type of request for the chat completion.
        :param functions: Functions used for the chat completion.
        :param json_response: Response from the chat completion in JSON format.
        """
        if not USE_GPTPILOT_FOLDER:
            return

        if self.log_chat_completions:
            time = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')

            with open(os.path.join(self.chat_log_path, f'{time}-{req_type}.json'), 'w', encoding="utf-8") as file:
                data = {
                    'endpoint': endpoint,
                    'model': model,
                    'functions': functions,
                    'response': json.loads(json_response),
                }

                json.dump(data, file, indent=2)

    def write_project(self, project):
        """
        Write the project data to a YAML file in the '.gpt-pilot' directory.

        :param project: Project object containing the project data.
        """
        if not USE_GPTPILOT_FOLDER:
            return

        data = {
            'name': project.
