import json
import os
import yaml
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
USE_GPTPILOT_FOLDER = os.getenv('USE_GPTPILOT_FOLDER') == 'true'

class DotGptPilot:
    def __init__(self, log_chat_completions=True):
        self.log_chat_completions = log_chat_completions
        self.dot_gpt_pilot_path = self.with_root_path('~', create=False)

    def with_root_path(self, root_path, create=True):
        dot_gpt_pilot_path = os.path.expanduser(os.path.join(root_path, '.gpt-pilot'))
        if create and self.log_chat_completions:
            self.chat_log_folder(None)
        return dot_gpt_pilot_path if USE_GPTPILOT_FOLDER else ''

    def chat_log_folder(self, task=None):
        chat_log_path = os.path.join(self.dot_gpt_pilot_path, 'chat_log')
        if task is not None:
            chat_log_path = os.path.join(chat_log_path, f'task_{task}')
        os.makedirs(chat_log_path, exist_ok=True)
        return chat_log_path if USE_GPTPILOT_FOLDER else ''

    def log_chat_completion(self, endpoint, model, req_type, messages, response):
        if not self.log_chat_completions:
            return

        time = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
        file_path = os.path.join(self.chat_log_folder(None), f'{time}-{req_type}.yaml')
        data = {
            'endpoint': endpoint,
            'model': model,
            'messages': messages,
            'response': response,
        }
        with open(file_path, 'w', encoding="utf-8") as file:
            yaml.safe_dump(data, file, width=120, indent=2, default_flow_style=False, sort_keys=False)

    def log_chat_completion_json(self, endpoint, model, req_type, functions, json_response):
        if not self.log_chat_completions:
            return

        time = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
        file_path = os.path.join(self.chat_log_folder(None), f'{time}-{req_type}.json')
        data = {
            'endpoint': endpoint,
            'model': model,
            'functions': functions,
            'response': json.loads(json_response),
        }
        with open(file_path, 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=2)

    def write_project(self, project):
        if not USE_GPTPILOT_FOLDER:
            return

        data = {
            'name': project.name,
            'description': project.description,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }

        file_path = os.path.join(self.dot_gpt_pilot_path, 'project.yaml')
        with open(file_path, 'w', encoding="utf-8") as file:
            yaml.safe_dump(data, file, width=120, indent=2, default_flow_style=False, sort_keys=False)
