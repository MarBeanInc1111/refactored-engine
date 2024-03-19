import hashlib
import os
import re
import sys
import uuid
from getpass import getuser
from database.database import get_app, get_app_by_user_workspace
from utils.style import color_green_bold, color_red, style_config
from utils.utils import should_execute_step
from const.common import STEPS

def get_arguments() -> dict:
    # The first element in sys.argv is the name of the script itself.
    # Any additional elements are the arguments passed from the command line.
    args = sys.argv[1:]

    # Create an empty dictionary to store the key-value pairs.
    arguments = {
        'continuing_project': False,
        'app_id': None,
        'user_id': None,
        'email': None,
        'password': None,
        'step': None,
        'workspace': None,
        'app_type': None,
        'name': None,
        'status': None,
        'theme': 'dark'
    }

    # Loop through the arguments and parse them as key-value pairs.
    for arg in args:
        if '=' in arg:
            key, value = arg.split('=', 1)
            arguments[key] = value
        else:
            arguments[arg] = True

    # Validate arguments
    validate_arguments(arguments)

    # Set theme
    theme_mapping = {'light': style_config.theme.LIGHT, 'dark': style_config.theme.DARK}
    style_config.set_theme(theme=theme_mapping.get(arguments['theme'], style_config.theme.DARK))

    # Set user_id
    if arguments['user_id'] is None:
        arguments['user_id'] = username_to_uuid(getuser())

    # Set app
    if arguments['workspace'] is not None:
        arguments['workspace'] = os.path.abspath(arguments['workspace'])
        app = get_app_by_user_workspace(arguments['user_id'], arguments['workspace'])
        if app is not None:
            arguments['app_id'] = str(app.id)
            arguments['continuing_project'] = True
            arguments['app_type'] = app.app_type
            arguments['name'] = app.name
            arguments['status'] = app.status
    else:
        arguments['workspace'] = None

    if arguments['app_id'] is None:
        arguments['app_id'] = str(uuid.uuid4())
        print_success(f'Starting new project with app_id: {arguments["app_id"]}')

    if arguments['step'] is None:
        arguments['step'] = get_next_step(arguments)

    return arguments

def validate_arguments(arguments: dict) -> None:
    required_arguments = ['app_id', 'user_id', 'email', 'password']
    for arg in required_arguments:
        if arguments[arg] is None:
            print_error(f'Error: Required argument {arg} is missing.')
            sys.exit(-1)

def print_usage() -> None:
    print('Usage: python script.py [options]')
    print('Options:')
    print('  app_id=<app_id>          The app id.')
    print('  user_id=<user_id>        The user id.')
    print('  email=<email>            The email.')
    print('  password=<password>      The password.')
    print('  workspace=<workspace>    The workspace.')
    print('  step=<step>              The step.')
    print('  theme=<theme>            The theme (light or dark).')

def should_execute_step(step: str, status: str) -> bool:
    if step is None or status is None:
        return False
    if step == 'all':
        return True
    if status == 'finished':
        return step == 'finished'
    if step == 'finished':
        return status == 'created'
    return STEPS.index(step) > STEPS.index(status)

def get_app_by_app_id(app_id: str) -> dict:
    app = get_app(app_id)
    if app is not None:
        return {
            'app_id': str(app.id),
            'app_type': app.app_type,
            'name': app.name,
            'status': app.status
        }
    return None

def get_username() -> str:
    return getuser()

def get_app_type_name(app_type: str) -> str:
    if app_type == 'web':
        return 'Web Application'
    if app_type == 'mobile':
        return 'Mobile Application'
    return 'Unknown'

def get_next_step(arguments: dict) -> str:
    if arguments['status'] == 'created':
        return STEPS[STEPS.index('created') + 1]
    return 'finished'

def print_banner() -> None:
    print_separator()
    print_loading('Loading project...')
    print_loading('Initializing environment...')
    print_loading('Setting up configuration...')
    print_loading('Checking dependencies...')
    print_separator()

def print_footer() -> None:
    print_success('Project
