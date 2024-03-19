import os
from helpers.agents import Developer, ENVIRONMENT_SETUP_STEP
from helpers import AgentConvo, Project
from helpers.files import update_file
from database import save_app

def run_command_until_success():
    # Function to set up and run a command until success

    # Assign a name for the project
    name = "run_command_until_success"

    # Initialize Project instance with given parameters
    project = Project(
        app_id="84c2c532-e07c-4694-bcb0-70767c348b07",
        name=name,
        app_type="",
        user_id="97510ce7-dbca-44b6-973c-d27346ce4009",
        email="7ed2f578-c791-4719-959c-dedf94394ad3",
        password="secret",
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
    project.app = save_app(project)

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

    # Set run_command for the developer
    developer.run_command = "npm install"
