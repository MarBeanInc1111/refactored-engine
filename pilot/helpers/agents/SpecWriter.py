from helpers.AgentConvo import AgentConvo  # Importing AgentConvo helper class from helpers.AgentConvo module
from helpers.Agent import Agent  # Importing Agent base class from helpers.Agent module
from utils.files import count_lines_of_code  # Importing count_lines_of_code utility function from utils.files module
from utils.style import color_green_bold, color_yellow_bold  # Importing color_green_bold and color_yellow_bold utility functions from utils.style module
from prompts.prompts import ask_user  # Importing ask_user function from prompts.prompts module
from const.messages import AFFIRMATIVE_ANSWERS  # Importing AFFIRMATIVE_ANSWERS constant from const.messages module
from utils.exit import trace_code_event  # Importing trace_code_event utility function from utils.exit module

INITIAL_PROJECT_HOWTO_URL = "https://github.com/Pythagora-io/gpt-pilot/wiki/How-to-write-a-good-initial-project-description"

class SpecWriter(Agent):  # Defining SpecWriter class that inherits from Agent base class
    def __init__(self, project):  # Constructor method with project parameter
        super().__init__('spec_writer', project)  # Calling Agent's constructor method with 'spec_writer' and project parameters
        self.save_dev_steps = True  # Setting save_dev_steps attribute to True

    def analyze_project(self, initial_prompt):  # Defining analyze_project method with initial_prompt parameter
        msg = (
            "Your project description seems a bit short. "
            "The better you can describe the project, the better GPT Pilot will understand what you'd like to build.\n\n"
            f"Here are some tips on how to better describe the project: {INITIAL_PROJECT_HOWTO_URL}\n\n"
        )
        print(color_yellow_bold(msg))  # Printing message in yellow color and bold font
        print(color_green_bold("Let's start by refining your project idea:"))  # Printing message in green color and bold font

        convo = AgentConvo(self)  # Creating AgentConvo object with self parameter
        convo.construct_and_add_message_from_prompt('spec_writer/ask_questions.prompt', {})  # Calling AgentConvo's method with prompt name and empty dictionary as parameters

        num_questions = 0  # Initializing num_questions variable to 0
        skipped = False  # Initializing skipped variable to False
        user_response = initial_prompt  # Assigning initial_prompt value to user_response variable
        while True:  # Infinite loop
            llm_response = convo.send_message('utils/python_string.prompt', {
                "content": user_response,
            })  # Calling AgentConvo's send_message method with prompt name and dictionary with 'content' key and user_response value as parameters
            if not llm_response:  # If llm_response is None or empty string
                continue  # Continue to the next iteration of the loop

            num_questions += 1  # Increment num_questions by 1
            llm_response = llm_response.strip()  # Removing leading and trailing whitespaces from llm_response
            if len(llm_response) > 500:  # If length of llm_response is greater than 500
                print('continue', type='button')  # Print 'continue' with type 'button'
                user_response = ask_user(
                    self.project,
                    "Can we proceed with this project description? If so, just press ENTER. Otherwise, please tell me what's missing or what you'd like to add.",
                    hint="Does this sound good, and does it capture all the information about your project?",
                    require_some_input=False
                )  # Calling ask_user function with project, prompt, hint, and require_some_input parameters
                if user_response:  # If user_response is not None or empty string
                    user_response = user_response.strip()  # Removing leading and trailing whitespaces from user_response
                if user_response.lower() in AFFIRMATIVE_ANSWERS + ['continue']:  # If user_response is in AFFIRMATIVE_ANSWERS list or 'continue' string
                    break  # Break the infinite loop
            else:
                print('skip questions', type='button')  # Print 'skip questions' with type 'button'
                user_response = ask_user(self.project,
