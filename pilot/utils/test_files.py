import os
from unittest.mock import patch
from utils.files import setup_workspace

def mock_makedirs(*args, **kwargs):
    return

@patch('utils.files.os.makedirs', mock_makedirs)
def test_setup_workspace():
    setup_workspace('test_workspace')
    assert os.path.exists('test_workspace'), 'Workspace directory should have been created'

