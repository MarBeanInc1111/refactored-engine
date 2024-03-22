import os
import time
from helpers.agents import Developer, ENVIRONMENT_SETUP_STEP
from helpers import AgentConvo, Project
from helpers.files import update_file
from database import save_app

def run_command_until_success(command, max_retries=5, delay=1):
    # Function to set up and run a command until success

    # Assign a name for the project
    name = "run_command_until_success"

    # Initialize Project instance with given parameters
    project = Project(
        app_id="<APP_ID>",
        name=name,
        app_type="",
        user_id="<USER_ID>",
        email="<EMAIL>",
        password="<PASSWORD>",
        architecture=[],
        user_stories=[]
    )

    # Set root path for the project
    project_root_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../workspace/TestDeveloper"))
    project.set_root_path(project_root_path)

    # Set technologies and current step for the project
    project.technologies = []
    project.current_step = ENVIRONMENT_SETUP_STEP

    # Save the app
    try:
        project.app = save_app(project)
    except Exception as e:
        print(f"Error saving app: {e}")
        return

    # Update package.json
    package_json_path = os.path.join(project_root_path, "package.json")
    package_dependencies = {
        "axios": "^1.5.0",
        "express": "^4.18.2",
        "mongoose": "^7.5.0"
    }
    update_file(package_json_path, {"dependencies": package_dependencies})

    # Initialize Developer instance
    developer = Developer(project)

    # Set run_
