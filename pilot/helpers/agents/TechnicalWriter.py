from const.function_calls import GET_DOCUMENTATION_FILE  # Importing the constant for documentation file
from helpers.AgentConvo import AgentConvo  # Importing AgentConvo helper class
from helpers.Agent import Agent  # Importing Agent base class
from utils.files import count_lines_of_code  # Importing function to count lines of code
from utils.style import color_green_bold, color_green  # Importing coloring functions for console output

class TechnicalWriter(Agent):  # Inheriting from Agent base class
    def __init__(self, project):
        super().__init__('technical_writer', project)  # Initializing the Agent base class
        self.save_dev_steps = True  # Attribute to save development steps

    def document_project(self, percent):
        files = self.project.get_all_coded_files()  # Getting all coded files from the project
        print(f'{color_green_bold("CONGRATULATIONS!!!")}', category='success')  # Printing congratulations message
        print(f'You reached {color_green(str(percent) + "%")} of your project generation!\n\n')  # Printing project progress
        print('For now, you have created:\n')  # Informing about the created files and lines of code
        print(f'{color_green(len(files))} files\n')
        print(f'{color_green(count_lines_of_code(files))} lines of code\n\n')
        print('Before continuing, GPT Pilot will create some documentation for the project...\n')  # Creating documentation
        print('', type='verbose', category='agent:tech-writer')  # Printing verbose message
        self.create_license()  # Creating a license
        self.create_readme()  # Creating a README file
        self.create_api_documentation()  # Creating API documentation

    def create_license(self):
        # check if LICENSE file exists and if not create one. We want to create it only once.
        pass  # Placeholder for creating a license file

    def create_readme(self):
        print(color_green('Creating README.md'))  # Printing message for creating README.md
        convo = AgentConvo(self)  # Initializing AgentConvo helper class

        # Sending a message to the LLM (Language Model) to create the README.md file
        llm_response = convo.send_message('documentation/create_readme.prompt', {
            "name": self.project.args['name'],
            "app_type": self.project.args['app_type'],
            "app_summary": self.project.project_description,
            "user_stories": self.project.user_stories,
            "user_tasks": self.project.user_tasks,
            "directory_tree": self.project.get_directory_tree(True),
            "files": self.project.get_all_coded_files(),
            "previous_features": self.project.previous_features,
            "current_feature": self.project.current_feature,
        }, GET_DOCUMENTATION_FILE)

        self.project.save_file(llm_response)  # Saving the generated README.md file
        return convo  # Returning the AgentConvo instance for potential further use

    def create_api_documentation(self):
        # create API documentation
        pass  # Placeholder for creating API documentation
