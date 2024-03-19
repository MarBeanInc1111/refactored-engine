import json
import re
import subprocess
import uuid
from os.path import sep
from typing import Dict, List

from database.database import save_development_step
from helpers.exceptions import TokenLimitError
from utils.function_calling import parse_agent_response
from utils.llm_connection import create_gpt_chat_completion
from utils.utils import get_prompt, get_sys_message, capitalize_first_word_with_underscores
from logger.logger import logger
from prompts.prompts import ask_user
from const.llm import END_RESPONSE
from utils.telemetry import telemetry

class ChatCompletionParams:
    def __init__(self, prompt_path: str, prompt_data: Dict):
        self.prompt_path = prompt_path
        self.prompt_data = prompt_data

class AgentConvo:
    """
    Represents a conversation with an agent.

    Args:
        agent: An instance of the agent participating in the conversation.
    """

    def __init__(self, agent, temperature: float = 0.7):
        self.messages: List[Dict] = []
        self.branches = {}
        self.log_to_user = True
        self.agent = agent
        self.high_level_step = self.agent.project.current_step
        self.chat_completion_params = {"temperature": temperature}

        system_message = get_sys_message(self.agent.role, self.agent.project.args)
        logger.info('\n>>>>>>>>>> System Prompt >>>>>>>>>>\n%s\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>',
                    system_message['content'])
        self.messages.append(system_message)

    def send_message(self, chat_completion_params: "ChatCompletionParams" = None, function_calls: FunctionCallSet = None, should_log_message=True):
        """
        Sends a message in the conversation.

        Args:
            chat_completion_params: The parameters for creating the chat completion.
            function_calls: Optional function calls to be included in the message.
            should_log_message: Flag if final response should be logged.
        Returns:
            The response from the agent.
        """
        if chat_completion_params is not None:
            self.chat_completion_params = chat_completion_params.__dict__

        # craft message
        self.construct_and_add_message_from_prompt(chat_completion_params.prompt_path, chat_completion_params.prompt_data)

        try:
            response = create_gpt_chat_completion(self.messages, self.high_level_step, self.agent.project,
                                                  function_calls=function_calls, prompt_data=chat_completion_params.prompt_data,
                                                  **self.chat_completion_params)
        except TokenLimitError as e:
            save_development_step(self.agent.project, chat_completion_params.prompt_path, chat_completion_params.prompt_data, self.messages, {"text": ""}, str(e))
            raise e

        if should_log_message:
            self.log_message(response)

        return response

    def format_message_content(self, response):
        if isinstance(response, str):
            return response
        else:
            return json.dumps(response)

    def construct_and_add_message_from_prompt(self, prompt_path, prompt_data):
        if prompt_path is not None and prompt_data is not None:
            prompt = get_prompt(prompt_path, prompt_data)
            logger.info('\n>>>>>>>>>> User Prompt >>>>>>>>>>\n%s\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', prompt)
            self.messages.append({"role": "user", "content": prompt})

    def replace_files_in_message(self, message, files_dict):
        replacement_lines = ["\n---START_OF_FILES---"]
        for path, content in files_dict.items():
            replacement_lines.append(f"**{path}** ({ len(content.splitlines()) } lines of code):\n```\n{content}\n```\
