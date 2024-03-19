import os
from unittest.mock import patch
from utils.files import setup_workspace

# Mock function for os.makedirs to avoid creating directories during testing
def mock_makedirs(*args, **kwargs):
    return

