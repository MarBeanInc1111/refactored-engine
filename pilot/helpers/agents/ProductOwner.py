import json
import os
from typing import Any

import colorama
from rich.console import Console
from rich.prompt import Prompt

colorama.init()
console = Console()

from helpers.AgentConvo import AgentConvo
from helpers.Agent import Agent
from helpers.database import get_app, save_app, save_progress
from helpers.files import setup_workspace
from helpers.project import clean_filename, should_execute_step
from helpers.utils import generate_app_data
from prompts.prompts import ask_for_app_type, ask_for_main_app_definition, ask_user
from const.llm import END_RESPONSE
from const.messages import MAX_PROJECT_NAME_LENGTH, PROJECT_DESCRIPTION_STEP
from const.common import EXAMPLE_PROJECT_DESCRIPTION

class ProductOwner(Agent):
    def __init__(self, project):
        super().__init__('product_owner', project)

    def get_project_description(self, spec_writer):
        console.log('[info][agent:product-owner] Project description stage', style='dim')

        app = get_app(self.project.args['app_id'], error_if_not_found=False)

        if app and should_execute_step(self.project.args['step'], PROJECT_DESCRIPTION_STEP):
            self.project.set_root_path(setup_workspace(self.project.args))
            self.project.project_description = app['summary']
            self.project.project_description_messages = app['messages']
            self.project.main_prompt = app['prompt']
            return

        self.project.current_step = PROJECT_DESCRIPTION_STEP

        app_type = self.project.args.get('app_type') or ask_for_app_type()
        project_name = self.get_project_name()

        self.project.args['name'] = clean_filename(project_name)
        self.project.args['app_type'] = app_type

        app = save_app(self.project)
        self.project.app = app

        self.project.set_root_path(setup_workspace(self.project.args))

        self.project.main_prompt = self.get_main_prompt(app_type, project_name)

    def get_project_name(self) -> str:
        question = 'What is the project name?'
        print(question)
        print('(start an example project)')

        project_name = Prompt.ask(question)

        if project_name.lower() == 'start an example project':
            print(EXAMPLE_PROJECT_DESCRIPTION)
            return 'Example Project'

        if len(project_name) > MAX_PROJECT_NAME_LENGTH:
            raise ValueError(f"Project name cannot be longer than {MAX_PROJECT_NAME_LENGTH} characters.")

        return project_name

    def get_main_prompt(self, app_type: str, project_name: str) -> str:
        if app_type == 'web':
            return self.get_web_app_prompt(project_name)

        return ''

    def get_web_app_prompt(self, project_name: str) -> str:
        print(
            "\nGPT Pilot currently works best for web app projects using Node, Express and MongoDB. "
            "You can use it with other technologies, but you may run into problems (eg. React might not work as expected).\n"
        )

        return ask_for_main_app_definition()
