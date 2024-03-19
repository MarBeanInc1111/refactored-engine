import platform  # Importing platform to get the current platform information
import questionary  # Importing questionary to create interactive command-line prompts
import sys  # Importing sys for accessing system-specific parameters and functions
from database.database import save_user_input  # Importing save_user_input function to save user inputs
from utils.style import style_config  # Importing style_config to get the preferred style
from utils.print import remove_ansi_codes  # Importing remove_ansi_codes to remove ANSI escape codes

def styled_select(*args, **kwargs):
    """
    A function to create a styled select prompt using questionary.
    This function allows users to select one option from a list of choices.

    Args:
    *args: Variable length argument list.
    **kwargs: Arbitrary keyword arguments.

    Returns:
    The selected option from the list of choices.
    """
    kwargs["style"] = style_config.get_style()
    # TODO add saving and loading of user input
    return questionary.select(*args, **kwargs).unsafe_ask()  # .ask() is included here


def styled_text(project, question, ignore_user_input_count=False, style=None, hint=None):
    """
    A function to ask the user a question and return the answer.
    This function handles colorama and questionary incompatibility issues and saves user inputs.

    Args:
    project: The project object.
    question: The question to be asked to the user.
    ignore_user_input_count: A boolean to ignore the user input count.
    style: The style to be used for the question.
    hint: The hint to be displayed for the question.

    Returns:
    The answer provided by the user.
    """
    if not ignore_user_input_count:
        project.user_inputs_count += 1

    if project is not None and project.check_ipc():
        response = print(question, type='user_input_request')
    else:
        used_style = style if style is not None else style_config.get_style()
        question = remove_ansi_codes(question)  # Colorama and questionary are not compatible and styling doesn't work
        flush_input()
        response = questionary.text(question, style=used_style).unsafe_ask()  # .ask() is included here

    if not ignore_user_input_count:
        save_user_input(project, question, response, hint)

    if project is not None and not project.check_ipc():
        print('\n\n', end='')
    return response


def get_user_feedback():
    """
    A function to get user feedback about the application.

    Returns:
    The feedback provided by the user.
    """
    return questionary.text('How did GPT Pilot do? Were you able to create any app that works? '
                            'Please write any feedback you have or just press ENTER to exit: ',
                            style=style_config.get_style()).unsafe_ask()


def ask_user_to_store_init_prompt():
    """
    A function to ask the user if they want to store the initial app prompt.

    Returns:
    The user's response to storing the initial app prompt.
    """
    return questionary.text('We would appreciate if you let us store your initial app prompt. '
                            'If you are OK with that, please just press ENTER',
                            style=style_config.get_style()).unsafe_ask()


def flush_input():
    """
    A function to flush the input buffer, discarding all that's in the buffer.
    """
    try:
        if platform.system() == 'Windows':
            import msvcrt
            while msvcrt.kbhit():
                msvcrt.getch()
        else
