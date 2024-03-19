import requests

from helpers.cli import terminate_running_processes  # For terminating running processes
from prompts.prompts import ask_user  # For getting user input

from utils.telemetry import telemetry  # For handling telemetry data

def send_feedback(feedback, path_id):
    """
    Send the collected feedback to the endpoint.

    This function sends feedback data to the specified API endpoint. It catches and logs any request exceptions.

    :param feedback: The feedback data to be sent
    :param path_id: The path identifier for the current execution
    """
    # Prepare the feedback data (you can adjust the structure as per your backend needs)
    feedback_data = {
        "pathId": path_id,
        "data": feedback,
        "event": "pilot-feedback"
    }

    try:
        response = requests.post("https://api.pythagora.io/telemetry", json=feedback_data)
        response.raise_for_status()  # Raise an exception if the status code is not 2xx
    except requests.RequestException as err:
        print(f"Failed to send feedback data: {err}")  # Log the error message


def trace_code_event(name: str, data: dict):
    """
    Record a code event to trace potential logic bugs.

    This function sends telemetry data for a specific event with additional data. If there's an exception, it doesn't raise it.

    :param name: name of the event
    :param data: data to send with the event
    """
    path_id = get_path_id()

    # Prepare the telemetry data
    telemetry_data = {
        "pathId": path_id,
        "event": f"trace-{name}",
        "data": data,
    }

    try:
        response = requests.post("https://api.pythagora.io/telemetry", json=telemetry_data)
        response.raise_for_status()  # Raise an exception if the status code is not 2xx
    except:  # noqa
        pass  # Ignore any exceptions during telemetry data sending


def get_path_id():
    """Return the path identifier for the current execution."""
    return telemetry.telemetry_id

def ask_to_store_prompt(project, path_id):
    """
    Ask the user if they want to store the initial app prompt.

    This function sends telemetry data for the "pilot-prompt" event with the initial app prompt if the user agrees.

    :param project: The project object
    :param path_id: The path identifier for the current execution
    """
    init_prompt = project.main_prompt if project is not None and project.main_prompt else None
    if init_prompt is None:
        return

    # Prepare the prompt data
    telemetry_data = {
        "pathId": path_id,
        "event": "pilot-prompt",
        "data": init_prompt
    }

    question = ('We would appreciate if you let us store your initial app prompt. If you are OK with that, please just '
                'press ENTER')

    try:
        answer = ask_user(project, question, ignore_user_input_count=True, require_some_input=False)
        if answer == '':
            telemetry.set("initial_prompt", init_prompt)
            response = requests.post("https://api.pythagora.io/telemetry", json=telemetry_data)
            response.raise_for_status()
    except requests.RequestException as err:
        print(f"Failed to store prompt: {err}")
    except KeyboardInterrupt:
        pass


def ask_user_feedback(project, path_id, ask_feedback):
    """
    Ask the user for feedback.

    This function sends telemetry data for the "pilot-feedback" event with the user's feedback if they provide any.

    :param project: The project object
    :param path_id: The path identifier for the current execution
    :param ask_feedback: A flag indicating whether to ask for feedback
    """
    question = ('Were you able to create any app that works? Please write any feedback you have or just press ENTER to exit:')
    feedback = None
    if ask_feedback:
        feedback = ask_user(project, question, ignore_user_input_count=True, require_some_input=False)
    if feedback:  # only send if user provided feedback
        telemetry.set("user_feedback", feedback)
        send_feedback(feedback, path_id)


def ask_user_email(project):
    """
    Ask the user for their email address.

    This function sends telemetry data for the "user_contact" event with the user's email address if they provide any.

    :param project: The project object
    :return: A flag indicating whether the user provided their email address
    """
    question = (
        "How did GPT Pilot do? We'd love to talk with you and hear your thoughts. "
        "If you'd like to be contacted by us, please provide your email address, or just press ENTER to exit:"
    )
    try:
        feedback = ask_user(project, question, ignore_user_input_count=True, require_some_input=False)
        if feedback:  # only send if user provided feedback
            telemetry.set("user_contact", feedback)
            return True
    except KeyboardInterrupt:
        pass
    return False

def exit_gpt_pilot(project, ask_feedback=True):
    """
    Terminate running processes and send telemetry data.

    This function terminates running processes, sends telemetry data, and prints the "Exit" message.

    :param project: The project object
    :param ask_feedback: A flag indicating whether to ask for feedback
    """
    terminate_running_processes()
    path_id = get_path_id()

    if ask_feedback:
        ask_to_
