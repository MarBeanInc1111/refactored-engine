import platform
import questionary
import sys
from database.database import save_user_input
from utils.style import style_config
from utils.print import remove_ansi_codes

def styled_select(*args, **kwargs):
    """
    Create a styled select prompt using questionary.
    Allow users to select one option from a list of choices.

    Returns:
        The selected option from the list of choices.
    """
    kwargs["style"] = style_config.get_style()
    return questionary.select(*args, **kwargs).ask()


def styled_text(project, question, ignore_user_input_count=False, style=None, hint=None):
    """
    Ask the user a question and return the answer.
    Handle colorama and questionary incompatibility issues and save user inputs.

    Args:
        project: The project object.
        question: The question to be asked to the user.
        ignore_user_input_count: Ignore the user input count.
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
        question = remove_ansi_codes(question)
        response = questionary.text(question, style=used_style).ask()

    if not ignore_user_input_count:
        save_user_input(project, question, response, hint)

    if project is not None and not project.check_ipc():
        print('\n\n', end='')
    return response


def get_user_feedback():
    """
    Get user feedback about the application.

    Returns:
        The feedback provided by the user.
    """
    return questionary.text('How did GPT Pilot do? Were you able to create any app that works? '
                            'Please write any feedback you have or just press ENTER to exit: ').ask()


def ask_user_to_store_init_prompt():
    """
    Ask the user if they want to store the initial app prompt.

    Returns:
        The user's response to storing the initial app prompt.
    """
    return questionary.text('We would appreciate if you let us store your initial app prompt. '
                            'If you are OK with that, please just press ENTER',
                            style=style_config.get_style()).ask()


def flush_input():
    """
    Flush the input buffer, discarding all that's in the buffer.
    """
    try:
        if platform.system() == 'Windows':
            import msvcrt
            while msvcrt.kbhit():
                msvcrt.getch()
        else:
            raise NotImplementedError(f"Flushing input not implemented for platform: {platform.system()}")
    except NotImplementedError as e:
        print(f"Error: {e}")
