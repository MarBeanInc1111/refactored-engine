import builtins
from typing import Any
from helpers.ipc import IPCClient
from const.ipc import MESSAGE_TYPE, LOCAL_IGNORE_MESSAGE_TYPES
from utils.print import remove_ansi_codes

def get_custom_print(args: dict) -> tuple:
    """
    This function returns a custom print function and an IPCClient instance based on the provided arguments.

    :param args: A dictionary of arguments
    :return: A tuple containing a custom print function and an IPCClient instance
    """
    built_in_print = builtins.print

    def print_to_external_process(*args: Any, **kwargs: Any) -> None:
        """
        This function prints the given message to an external process through an IPCClient instance.

        :param args: Variable length argument list
        :param kwargs: Variable length keyword argument dictionary
        :return: None
        """
        # Extracting the message from the arguments
        message = args[0]

        # Setting the default message type to 'verbose' if it's not provided
        message_type = kwargs.get('type', 'verbose')

        # Checking if the message type is local and if so, printing it locally
        if message_type == MESSAGE_TYPE['local']:
            local_print(*args, **kwargs)
            return

        # Sending the message to the external process through the IPCClient instance
        ipc_client_instance.send({
            'type': MESSAGE_TYPE[message_type],
            'category': kwargs.get('category', ''),
            'content': remove_ansi_codes(message),
        })

        # If the message type is 'user_input_request', listen for a response from the external process
        if message_type == MESSAGE_TYPE['user_input_request']:
            return ipc_client_instance.listen

    def local_print(*args: Any, **kwargs: Any) -> None:
        """
        This function prints the given message locally.

        :param args: Variable length argument list
        :param kwargs: Variable length keyword argument dictionary
        :return: None
        """
        built_in_print(*args, **kwargs)

    ipc_client_instance = IPCClient(**args.get('ipc', {}))
    return print_to_external_process, ipc_client_instance
