from helpers.AgentConvo import AgentConvo
from helpers.Agent import Agent
from utils.files import count_lines_of_code
from utils.style import color_green_bold, color_yellow_bold
from prompts.prompts import ask_user
from const.messages import AFFIRMATIVE_ANSWERS
from utils.exit import trace_code_event

INITIAL_PROJECT_HOWTO_URL = "https://github.com/Pythagora-io/gpt-pilot/wiki/How-to-write-a-good-initial-project-description"

class SpecWriter(Agent):
    """Defines a SpecWriter class that inherits from Agent base class."""

    def __init__(self, project):
        """Constructor method with project parameter.

        Args:
            project (Project): The project object.
        """
        super().__init__('spec_writer', project)
        self.save_dev_steps = True

    def analyze_project(self, initial_prompt: str) -> None:
        """Analyzes the project and refines the project idea.

        Args:
            initial_prompt (str): The initial prompt from the user.
        """
        msg = (
            "Your project description seems a bit short. "
            "The better you can describe the project, the better GPT Pilot will understand what you'd like to build.\n\n"
            f"Here are some tips on how to better describe the project: {INITIAL_PROJECT_HOWTO_URL}\n\n"
        )
        print(color_yellow_bold(msg))
        print(color_green_bold("Let's start by refining your project idea:"))

        convo = AgentConvo(self)
        convo.construct_and_add_message_from_prompt('spec_writer/ask_questions.prompt', {})

        num_questions = 0
        skipped = False
        user_response = initial_prompt
        while True:
            if not user_response:
                continue

            num_questions += 1
            llm_response = convo.send_message('utils/python_string.prompt', {
                "content": user_response,
            })
            if not llm_response:
                continue

            if len(llm_response) > 500:
                print('continue', type='button')
                user_response = ask_user(
                    self.project,
                    "Can we proceed with this project description? If so, just press ENTER. Otherwise, please tell me what's missing or what you'd like to add.",
                    hint="Does this sound good, and does it capture all the information about your project?",
                    require_some_input=False
                )
                if user_response and user_response.lower() not in AFFIRMATIVE_ANSWERS:
                    convo.construct_and_add_message_from_prompt('spec_writer/ask_questions.prompt', {})
            else:
                print('skip questions', type='button')
                break

        self.project.description = user_response
