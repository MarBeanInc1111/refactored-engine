import json
from utils.style import color_green_bold
from helpers.AgentConvo import AgentConvo
from helpers.Agent import Agent
from logger.logger import logger
from database.database import get_app, save_progress, save_app, get_progress_steps
from utils.utils import should_execute_step, generate_app_data, step_already_finished, clean_filename
from utils.files import setup_workspace
from prompts.prompts import ask_for_app_type, ask_for_main_app_definition, ask_user
from const.llm import END_RESPONSE
from const.messages import MAX_PROJECT_NAME_LENGTH
from const.common import EXAMPLE_PROJECT_DESCRIPTION

# Define the class for the product owner agent
class ProductOwner(Agent):
    # Initialize the product owner agent with the project object
    def __init__(self, project):
        super().__init__('product_owner', project)

    def get_project_description(self, spec_writer):
        """
        Get the project description from the user.

        This method initializes the project with the given app ID, and if the app ID has already completed this step,
        it loads the project description from the database and skips the user input. Otherwise, it asks the user
        for the project name and type, initializes the project workspace, and saves the project description in
        the database.

        :param spec_writer: The spec writer object
        """

        # Log the project stage
        print(json.dumps({
            "project_stage": "project_description"
        }), type='info', category='agent:product-owner')

        # Initialize the project app with the given app ID
        self.project.app = get_app(self.project.args['app_id'], error_if_not_found=False)

        # If this app ID already did this step, just get all data from DB and don't ask user again
        if self.project.app is not None:
            step = get_progress_steps(self.project.args['app_id'], PROJECT_DESCRIPTION_STEP)
            if step and not should_execute_step(self.project.args['step'], PROJECT_DESCRIPTION_STEP):
                step_already_finished(self.project.args, step)
                self.project.set_root_path(setup_workspace(self.project.args))
                self.project.project_description = step['summary']
                self.project.project_description_messages = step['messages']
                self.project.main_prompt = step['prompt']
                return

        # PROJECT DESCRIPTION
        self.project.current_step = PROJECT_DESCRIPTION_STEP
        is_example_project = False

        # Ask the user for the app type if it's not provided
        if 'app_type' not in self.project.args:
            self.project.args['app_type'] = ask_for_app_type()

        # Ask the user for the project name
        while True:
            question = 'What is the project name?'
            print(question, type='ipc')
            print('start an example project', type='button')
            project_name = ask_user(self.project, question)

            # Check if the project name is within the maximum length
            if len(project_name) <= MAX_PROJECT_NAME_LENGTH:
                break
            else:
                print(f"Hold your horses cowboy! Please, give project NAME with max {MAX_PROJECT_NAME_LENGTH} characters.")

        # Start an example project if the user selected it
        if project_name.lower() == 'start an example project':
            is_example_project = True
            project_name = 'Example Project'

        # Clean and set the project name
        self.project.args['name'] = clean_filename(project_name)

        # Save the project app in the database
        self.project.app = save_app(self.project)

        # Set up the project workspace
        self.project.set_root_path(setup_workspace(self.project.args))

        # Initialize the main prompt for the project
        if is_example_project:
            print(EXAMPLE_PROJECT_DESCRIPTION)
            self.project.main_prompt = EXAMPLE_PROJECT_DESCRIPTION
        else:
            print(color_green_bold(
                "GPT Pilot currently works best for web app projects using Node, Express and MongoDB. "
                "You can use it with other technologies, but you may run into problems "
                "(eg. React might not work as expected).\n"
            ))

            # Ask the user for the main app definition
            self.project.main_prompt = ask_for_main_
