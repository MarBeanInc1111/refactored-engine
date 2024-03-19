import os
import pathlib

APP_TYPES = ['Web App', 'Script', 'Mobile App', 'Chrome Extension']

ROLES = {
    'product_owner': ['project_description', 'user_stories', 'user_tasks'],
    'architect': ['architecture'],
    'tech_lead': ['development_planning'],
    'full_stack_developer': ['coding'],
    'dev_ops': ['environment_setup'],
    'code_monkey': ['coding']
}

STEPS = [
    'project_description',
    'user_stories',
    'user_tasks',
    'architecture',
    'environment_setup',
    'development_planning',
    'coding',
    'finished'
]

DEFAULT_IGNORE_PATHS = [
    '.git',
    '.gpt-pilot',
    '.idea',
    '.vscode',
    '.next',
    '.DS_Store',
    '__pycache__',
    "site-packages",
    'node_modules',
    'package-lock.json',
    'venv',
    'dist',
    'build',
    'target',
    "*.min.js",
    "*.min.css",
    "*.svg",
    "*.csv",
    "*.log",
    "go.sum",
]


def parse_ignore_paths(paths: str) -> list[str]:
    """Parse ignore paths from environment variable.

    Args:
        paths (str): Comma-separated list of ignore paths.

    Returns:
        list[str]: List of ignore paths.
    """
    return list(set(paths.split(','))) if paths else []


IGNORE_PATHS = DEFAULT_IGNORE_PATHS + parse_ignore_paths(os.environ.get('IGNORE_PATHS', ''))
IGNORE_SIZE_THRESHOLD = 50000  # 50K+ files are ignored by default
PROMPT_DATA_TO_IGNORE = {'directory_tree', 'name'}


def get_size(path: pathlib.Path) -> int:
    """Get the size of a file or directory.

    Args:
        path (pathlib.Path): Path of the file or directory.

    Returns:
        int: Size in bytes.
    """
    if path.is_file():
        return path.stat().st_size
    elif path.is_dir():
        return sum(get_size(child) for child in path.glob('*') if child.is_file())
    else:
        return 0


def get_app_type(app_type: str) -> str:
    """Get the type of an app.

    Args:
        app_type (str): Type of the app.

    Returns:
        str: The app type.
    """
    return app_type.capitalize() if app_type else 'Unknown'


def get_role_responsibilities(role: str) -> list[str]:
    """Get the responsibilities of a role.

    Args:
        role (str): Role.

    Returns:
        list[str]: List of responsibilities.
    """
    return ROLES.get(role.lower(), [])


def get_steps_for_role(role: str) -> list[str]:
    """Get the steps for a role.

    Args:
        role (str): Role.

    Returns:
        list[str]: List of steps.
    """
    return [step for step in STEPS if step in get_role_responsibilities(role)]


def print_example_project_description() -> None:
    """Print the example project description.
    """
    print(EXAMPLE_PROJECT_DESCRIPTION)


EXAMPLE_PROJECT_DESCRIPTION = (
    "A simple webchat application in node/express using MongoDB. "
    "Use Bootstrap and jQuery on the frontend, for a simple, clean UI. "
    "Use socket.io for real-time communication between backend and frontend.\n\n"
    "Visiting <http://localhost:3000/>, users must first log in or create an account using "
    "a username and a password (no email required).\n\n"
    "Once authenticated, on the home screen users see list of active chat rooms and a button to create a new chat. "
    "They can either click a link to one of the chat rooms which redirects them to `/<chat-id>/` "
    "or click the button to create a new chat. Creating a new chat should ask for the chat name, "
    "and then create a new chat with that name (which doesn't need to be unique), and a unique chat id. "
    "The user should then be redirected to the chat page.\n\n"
    "Chat page should have the chat name as the title. There's no possibility to edit chat name. "
    "Below that, show previous messages in the chat (these should get loaded from the database "
