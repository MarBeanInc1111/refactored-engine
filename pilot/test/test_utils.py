from unittest.mock import Mock  # Importing Mock class from unittest.mock module


def mock_terminal_size():  # Defining a function named mock_terminal_size
    mock_size = Mock()  # Creating a Mock object
    mock_size.columns = 80  # Setting the columns attribute of the Mock object to 80
    return mock_size  # Returning the Mock object


def assert_non_empty_string(value):  # Defining a function named assert_non_empty_string
    assert isinstance(value, str)  # Asserting that the value is an instance of str
    assert len(value) > 0  # Asserting that the length of the value is greater than 0
