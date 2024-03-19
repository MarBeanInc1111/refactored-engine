import builtins  # Importing the built-in 'print' function from Python's builtins module
from helpers.ipc import IPCClient  # Importing IPCClient class from helpers.ipc module
from const.ipc import MESSAGE_TYPE, LOCAL_IGNORE_MESSAGE_TYPES  # Importing MESSAGE_TYPE and LOCAL_IGNORE_MESSAGE_TYPES constants from const.ipc module
from utils.print import remove_ansi_codes  # Importing remove_ansi_codes function from utils.print module

def get_custom_print(args):
    """
    This function returns a custom print function and an IPCClient instance based on the provided arguments.
    
    :param args: A dictionary of arguments
    :return: A tuple containing a custom print function and an IPCClient instance
    """
    built_in_print = builtins.print  # Assigning the built-in 'print' function to a local variable

    def print_to_external_process(*args, **kwargs):
        """
        This function prints the given message to an external process through an IPCClient instance.
        
        :param args: Variable length argument list
        :param kwargs: Variable length keyword argument dictionary
        :return: None
        """
        # Extracting the message from the arguments
        message = args[0]

        # Setting the default message type to 'verbose' if it's not provided
        if 'type' not in kwargs:
            kwargs['type'] = 'verbose'
        elif kwargs['type'] == MESSAGE_TYPE['local']:
            local_print(*args, **kwargs)  # If the message type is 'local', print the message locally
            return

        # Sending the message to the external process through the IPCClient instance
        ipc_client_instance.send({
            'type': MESSAGE_TYPE[kwargs['type']],
            'category': kwargs['category'] if 'category' in kwargs else '',
            'content': remove_ansi_codes(message),
        })

        # If the message type is 'user_input_request', listen for a response from the external process
        if kwargs['type'] == MESSAGE_TYPE['user_input_request']:
            return ipc_client_instance.listen

    def local_print(*args, **kwargs):
        """
        This function prints the given message locally.
        
        :param args: Variable length argument list
        :param kwargs: Variable length keyword argument dictionary
        :return: None
        """

