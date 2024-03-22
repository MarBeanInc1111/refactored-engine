import platform
import uuid
import re
import json
from const.messages import WHEN_USER_DONE, AFFIRMATIVE_ANSWERS, NEGATIVE_ANSWERS, STUCK_IN_LOOP, NONE_OF_THESE
from utils.exit import trace_code_event
from utils.style import (
    color_green,
    color_green_bold,
    color_red,
    color_red_bold,
    color_yellow_bold,
    color_cyan_bold,
    color_white_bold
)
from helpers.exceptions import TokenLimitError, TooDeepRecursionError
from helpers.Debugger import Debugger
from utils.questionary import styled_text
from utils.utils import step_already_finished
from helpers.agents.CodeMonkey import CodeMonkey
from logger.logger import logger
from helpers.Agent import Agent
from helpers.AgentConvo import AgentConvo
from utils.utils import should_execute_step, array_of_objects_to_string, generate_app_data
from helpers.cli import run_command_until_success, execute_command_and_check_cli_response
from const.function_calls import (EXECUTE_COMMANDS, GET_TEST_TYPE, IMPLEMENT_TASK, COMMAND_TO_RUN,
                                  ALTERNATIVE_SOLUTIONS, GET_BUG_REPORT_MISSING_DATA)
from database.database import save_progress, get_progress_steps, update_app_status
from utils.telemetry import telemetry
from prompts.prompts import ask_user
from utils.print import print_task_progress, print_step_progress

ENVIRONMENT_SETUP_STEP = 'environment_setup'

class Developer(Agent):
    def __init__(self, project):
        super().__init__('full_stack_developer', project)
        self.review_count = 0
        self.run_command = None
        self.save_dev_steps = True
        self.debugger = Debugger(self)

    def start_coding(self, task_source):
        """
        Starts the development process for the project.
        """
        print('Starting development...', type='verbose', category='agent:developer')
        if not self.project.finished:
            self.project.current_step = 'coding'
            update_app_status(self.project.args['app_id'], self.project.current_step)

        if not self.project.skip_steps:
            logger.info("Starting to create the actual code...")

        total_tasks = len(self.project.development_plan)
        documented_thresholds = {50}

        for i, dev_task in enumerate(self.project.development_plan):
            if not self.project.skip_steps:
                current_progress_percent = round((i / total_tasks) * 100, 2)

                for threshold in documented_thresholds:
                    if current_progress_percent > threshold and threshold not in documented_thresholds:
                        if not self.project.skip_steps:
                            self.project.technical_writer.document_project(current_progress_percent)
                            print('', type='verbose', category='agent:developer')
                        documented_thresholds.add(threshold)

            if self.project.tasks_to_load:
                task = self.project.tasks_to_load.pop(0)
                self.project.cleanup_list('dev_steps_to_load', task['id'])

                if len(self.project.tasks_to_load):
                    continue
                else:
                    readme_dev_step = next((el for el in self.project.dev_steps_to_load if
