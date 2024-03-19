import os                                 # Importing os module for file operations
from unittest.mock import patch            # Importing patch decorator for mocking functions
from utils.files import setup_workspace   # Importing the function to be tested

# Mock function for os.makedirs to avoid creating directories during testing
def mocked_create_directory(path, exist_ok=True):
    return                                 # Return without any action

# Mock function for os.path.abspath to return a constant path during testing
def mocked_abspath(file):
    return "/root_path/pilot/helpers"

@patch('utils.files.os.makedirs', side_effect=mocked_create_directory)  # Mocking os.makedirs
def test_setup_workspace_with_existing_workspace(mock_makedirs):
    args = {'workspace': '/some/directory', 'name': 'sample'}             # Test case with existing workspace
    result = setup_workspace(args)
    assert result == '/some/directory'      # Asserting the result to be the same as the input workspace

def test_setup_workspace_with_root_arg(monkeypatch):                      # Test case with root argument
    args = {'root': '/my/root', 'name': 'project_name'}

    monkeypatch.setattr('os.path.abspath', mocked_abspath)               # Mocking os.path.abspath
    monkeypatch.setattr('os.makedirs', mocked_create_directory)           # Mocking os.makedirs

    result = setup_workspace(args)
    assert result.replace('\\', '/') == "/my/root/workspace/project_name"  # Asserting the result with expected path

@patch('utils.files.os.path.abspath', return_value='/root_path/pilot/helpers')  # Mocking os.path.abspath
@patch('utils.files.os.makedirs', side_effect=mocked_create_directory)          # Mocking os.m
