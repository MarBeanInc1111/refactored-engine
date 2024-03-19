import requests
from typing import Dict, Any

import helpers.cli  # For terminating running processes
import prompts.prompts  # For getting user input
import utils.telemetry  # For handling telemetry data

def send_feedback(feedback: Dict[str, Any], path_id: str) -> None:
    """
    Send the collected feedback to the endpoint.

    This function sends feedback data to the specified API endpoint. It catches and logs any request exceptions.

    :param feedback: The feedback data to be sent
    :param path_id: The path identifier for the current execution
    """
    feedback_data = {
        "pathId": path_id,
        "data": feedback,
        "event": "pilot-feedback",
    }

    try:
        response = requests.post("https://api.pythagora.io/telemetry", json=feedback_data)
        response.raise_for_status()
    except requests.RequestException as err:
        print(f"Failed to send feedback data: {err}")


def trace_code_event(name: str, data: Dict[str, Any]) -> None:
    """
    Record a code event to trace potential logic bugs.

    This function sends telemetry data for a specific event with additional data. If there's an exception, it doesn't raise it.

    :param name: name of the event
    :param data: data to send with the event
    """
    path_id = get_path_id()

    telemetry_data = {
        "pathId": path_id,
        "event": f"trace-{name}",
        "data": data,
    }

    try:
        requests.post("https://api.pythagora.io/telemetry", json=telemetry_data)
    except requests.RequestException:  # noqa
        pass  # Ignore any exceptions during telemetry data sending


def get_path_id() -> str:
    """Return the path identifier for the current execution."""
    return utils.telemetry.telemetry_id


def ask_to_store_prompt(project, path_id: str) -> None:
    """
    Ask the user if they want to store the initial app prompt.

    This function sends telemetry data for the "pilot-prompt" event with the initial app prompt if the user agrees.

    :param project: The project object
    :param path_id: The path identifier for the current execution
    """
    init_prompt = project.main_prompt if project is not None else None
    if init_prompt is None:
        return

    telemetry_data = {
        "pathId": path_id,
        "event": "pilot-prompt",
        "data": init_prompt,
    }

    question = (
        "We would appreciate if you let us store your initial app prompt. If you are OK with that, please just press ENTER."
    )

    try:
        answer = prompts.prompts.ask_user(project, question, ignore_user_input_count=True, require_some_input=False)
        if answer == "":
            utils.telemetry.telemetry.set("initial_prompt", init_prompt)
            send_feedback(telemetry_data, path_id)
    except requests.RequestException as err:
        print(f"Failed to store prompt: {err}")
    except KeyboardInterrupt:
        pass


def ask_user_feedback(project, path_id: str, ask_feedback: bool) -> None:
    """
    Ask the user for feedback.

    This function sends telemetry data for the "pilot-feedback" event with the user's feedback if they provide any.

    :param project: The project object
    :param path_id: The path identifier for the current execution
    :param ask_feedback: A flag indicating whether to ask for feedback
    """
    question = (
        "Were you able to create any app that works? Please write any feedback you have or just press ENTER to exit."
    )
    feedback = None
    if ask_feedback:
        feedback = prompts.prompts.ask_user(
            project, question, ignore_user_input_count=True, require_some_input=False
        )
    if feedback:  # only send if user provided feedback
        utils.telemetry.telemetry.set("user_feedback", feedback)
        send_feedback(feedback, path_id)


def ask_user_email(project) -> bool:
    """
    Ask the user for their email address.

    This function sends telemetry data for the "user_contact" event with the user's email address if they provide any.

    :param project: The project object
    :return: A flag indicating whether the user provided their email address
    """
    question = (
        "How did GPT Pilot do? We'd love to talk with you and hear your thoughts. "
        "If you'd like to be contacted by us, please provide your email address, or just press ENTER to exit."
    )

    try:
        feedback = prompts.prompts.ask_user(
            project, question, ignore_user_input_count=True, require_some_input=False
        )
        if feedback:  # only send if user provided feedback
            utils.telemetry.telemetry.set("user_contact", feedback)
            return True
    except KeyboardInterrupt:
        pass
    return False


def exit_gpt_pilot(project, ask_feedback=True) -> None:
    """
    Terminate running processes and send telemetry data.

    This function terminates running processes, sends telemetry data, and prints the "Exit" message.

    :param project: The project object
    :param ask_feedback: A flag indicating whether to ask for feedback
    """
    helpers.cli.terminate_running_processes()
    path_id = get_path_id()

    if ask_feedback:
        ask_to_store_prompt(project, path_id
