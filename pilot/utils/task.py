import json
import uuid
from typing import Any, Dict, List, Optional

from utils.telemetry import telemetry

class Task:
    """
    Task data structure to store information about the current task.
    The task data structure is sent to telemetry.
    Currently used to trace big loops in the code.
    """

    def __init__(self):
        self.initial_data = {
            'task_description': '',
            'task_number': 0,
            'steps': 0,
            'iterations': 0,
            'debugging': [],
        }
        self.data = self.initial_data.copy()
        self.ping_extension = True

    def set(self, key: str, value: Any) -> None:
        """
        Set a value in the task data

        :param key: key to set
        :param value: value to set
        """
        if not isinstance(key, str) or not isinstance(value, Any):
            raise TypeError("Key and value must be of type str and Any respectively")
        self.data[key] = value

    @property
    def steps(self) -> int:
        """
        Get the current number of steps

        :return: int
        """
        return self.data['steps']

    @steps.setter
    def steps(self, value: int) -> None:
        """
        Set the number of steps

        :param value: int
        """
        if not isinstance(value, int):
            raise TypeError("Value must be of type int")
        self.data['steps'] = value

    @steps.deleter
    def steps(self) -> None:
        """
        Delete the number of steps
        """
        del self.data['steps']

    @property
    def iterations(self) -> int:
        """
        Get the current number of iterations

        :return: int
        """
        return self.data['iterations']

    @iterations.setter
    def iterations(self, value: int) -> None:
        """
        Set the number of iterations

        :param value: int
        """
        if not isinstance(value, int):
            raise TypeError("Value must be of type int")
        self.data['iterations'] = value

    @iterations.deleter
    def iterations(self) -> None:
        """
        Delete the number of iterations
        """
        del self.data['iterations']

    def inc(self, key: str, value: int = 1) -> None:
        """
        Increment a value in the task data

        :param key: key to increment
        :param value: value to increment by
        """
        if not isinstance(key, str) or not isinstance(value, int):
            raise TypeError("Key and value must be of type str and int respectively")
        self.data[key] += value
        if key == 'iterations' and self.data[key] == LOOP_THRESHOLD + 1:
            self.send()

    def start_new_task(self, task_description: str, i: int) -> None:
        """
        Start a new task

        :param task_description: description of the task
        :param i: task number
        """
        self.send(name='loop-end')
        self.clear()
        self.set('task_description', task_description)
        self.set('task_number', i)
        self.set('loopId', f"{uuid.uuid4()}")

    def add_debugging_task(
        self,
        recursion_layer: Optional[int] = None,
        command: Optional[Dict[str, Any]] = None,
        user_input: Optional[str] = None,
        issue_description: Optional[str] = None,
    ) -> None:
        """
        Add a debugging task to the task data structure

        :param recursion_layer: recursion layer
        :param command: command to debug
        :param user_input: user input
        :param issue_description: description of the issue
        """
        self.data['debugging'].append({
            'recursion_layer': recursion_layer,
            'command': command,
            'user_inputs': [user_input] if user_input is not None else [],
            'issue_description': issue_description,
        })

    def add_user_input_to_debugging_task(self, user_input: str) -> None:
        """
        Add user input to the last debugging task

        :param user_input: user input
        """
        if self.data.get('debugging') and len(self.data['debugging']) > 0:
            self.data['debugging'][-1]['user_inputs'].append(user_input)

    def clear(self) -> None:
        """
        Clear all the task data
        """
        self.data = self.initial_data.copy()

    def send(self, name: str = 'loop-start', force: bool = False) -> None:
        """
        Send the task data to telemetry

        :param name: name of the event
        :param force: force send the task data to telemetry
        """
        if self.data['iterations'] > LOOP_THRESHOLD or force:
            full_data = telemetry.data.copy()
            full_data['task_with_loop'] = self.data.copy()
            trace_code_event(name=name, data=full_data)
            if self.ping_extension and not force:
                print(json.dumps({
                    'pathId': telemetry.telemetry_id,
                    'data': full_data
