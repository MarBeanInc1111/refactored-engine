import platform
import uuid
import re
import traceback
from typing import List, Dict, Any

import numpy as np

# Importing necessary modules for code execution, exceptions, logging, prompts, and utils.
from const.code_execution import MAX_COMMAND_DEBUG_TRIES, MAX_RECURSION_LAYER
from const.function_calls import DEBUG_STEPS_BREAKDOWN
from const.messages import AFFIRMATIVE_ANSWERS, NEGATIVE_ANSWERS
from helpers.AgentConvo import AgentConvo
from helpers.exceptions import TokenLimitError
from helpers.exceptions import TooDeepRecursionError
from logger.logger import logger
from prompts.prompts import ask_user
from utils.exit import trace_code_event
from utils.print import print_task_progress

class Debugger:
    def __init__(self, agent):
        # Initializing the Debugger class with an agent object.
        self.agent = agent
        self.recursion_layer = 0

    def debug(self, convo, command: dict = None, user_input: str = None, issue_description: str = None,
              is_root_task: bool = False, ask_before_debug: bool = False, task_steps: List[Dict[str, Any]] = None,
              step_index: int = None) -> bool:
        # Main debugging function that takes in conversation, command, user_input, issue_description,
        # is_root_task, ask_before_debug, task_steps, and step_index as arguments.

        # Incrementing recursion_layer by 1.
        self.recursion_layer += 1

        # Adding debugging task to the current task with the provided arguments.
        self.agent.project.current_task.add_debugging_task(self.recursion_layer, command, user_input, issue_description)

        # Checking if recursion_layer exceeds the maximum recursion layer allowed.
        if self.recursion_layer > MAX_RECURSION_LAYER:
            self.recursion_layer = 0
            # Raising TooDeepRecursionError if recursion_layer exceeds the maximum recursion layer allowed.
            raise TooDeepRecursionError()

        # Generating a unique function uuid.
        function_uuid = str(uuid.uuid4())

        # Saving a branch of the conversation with the generated function uuid.
        convo.save_branch(function_uuid)

        # Initializing success as False.
        success = False

        # Looping through the maximum command debug tries allowed.
        for i in range(MAX_COMMAND_DEBUG_TRIES):
            if success:
                break

            # Checking if user input is provided or if it's not the first iteration of the loop.
            if ask_before_debug or i > 0:
                # Asking the user for permission to start debugging and getting the answer.
                answer = ask_user(self.agent.project, 'Can I start debugging this issue [Y/n/error details]?',
                                  require_some_input=False)

                # Checking if the user wants to cancel debugging.
                if answer.lower() in NEGATIVE_ANSWERS:
                    self.recursion_layer -= 1
                    convo.load_branch(function_uuid)
                    return True

                # Checking if the user provided error details.
                if answer:
                    user_input = answer
                    self.agent.project.current_task.add_user_input_to_debugging_task(user_input)

            # Printing a debug message.
            print('', type='verbose', category='agent:debugger')

            # Sending a message to the developer with the provided arguments.
            try:
                llm_response = convo.send_message('dev_ops/debug.prompt',
                                                  {
                                                      'command': command['command'] if command is not None else None,
                                                      'user_input': user_input,
                                                      'issue_description': issue_description,
                                                      'task_steps': task_steps,
                                                      'step_index': step_index,
                                                      'os': platform.system()
                                                  },
                                                  DEBUG_STEPS_BREAKDOWN)
            except Exception as e:
                trace_code_event(e)
                continue

            # Initializing completed_steps as an empty list.
            completed_steps = []

            # Printing the task progress.
            print_task_progress(i + 1, i + 1, user_input, 'debugger', 'in_progress')

            # Trying to execute the task with the provided arguments.
            try:
                steps = completed_steps + llm_response['steps']

                # Executing the task with the provided steps.
                result = self.agent.project.developer.execute_task(
                    convo,
                    steps,
                    test_command=command,
                    test_after_code_changes=True,
                    continue_development=False,
                    is_root_task=is_root_task,
                    continue_from_step=len(completed_steps),
                    task_source='debugger',
                )

                # Checking if the step index is provided in the result.
                if 'step_index' in result:
                    # Updating the task with the provided result.
                    result['os'] = platform.system()
                    step_index = result['step_index']
                    completed_steps = steps[:step_index + 1]
                    result['completed_steps'] = completed_steps
                    result['current_step'] = steps[step_index]
                    result['next_steps'] = steps[step_index + 1:]
                    result['current_step_index'] = step_index

                    # Removing the previous debug plan and building a new one.
                    convo.remove_last_x_messages(2)
