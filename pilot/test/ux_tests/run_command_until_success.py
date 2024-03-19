import os
from helpers.agents import Developer, ENVIRONMENT_SETUP_STEP # Import Developer class and ENVIRONMENT_SETUP_STEP constant
from helpers import AgentConvo, Project # Import Project and AgentConvo classes
from helpers.files import update_file # Import update_file function
from database import save_app # Import save_app function

def run_command_until_success():
    # Function to set up and run a command until success
    name = 'run_command_until_success' # Assign a name for the project
    project = Project({\
        'app_id': '84c2c532-e07c-4694-bcb0-70767c348b07', # Set app_id
        'name': name, # Set project name
        'app_type': '', # Leave app_type empty
        'user_id': '97510ce7-dbca-44b6-973c-d27346ce4009', # Set user_id
        'email': '7ed2f578-c791-4719-959c-dedf94394ad3', # Set email
        'password': 'secret' # Set password
    }, name=name, architecture=[], user_stories=[]) # Initialize Project instance with given parameters

    project.set_root_path(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                     '../../../workspace/TestDeveloper')))
    project.technologies = [] # Set technologies
    project.current_step = ENVIRONMENT_SETUP_STEP # Set current step
    project.app = save_app(project) # Save the app

    update_file(f'{project.root_path}/package.json', {"dependencies": {"axios": "^1.5.0", "express": "^4.18.2", "mongoose": "^7.5.0"}}) # Update package.json

    developer = Developer(project) # Initialize Developer instance
    developer.run_command = 'npm install' # Set run_
