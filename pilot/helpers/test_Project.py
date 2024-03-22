import os
import json
from typing import Tuple

import pytest
from unittest.mock import patch
from helpers.Project import Project

test_root = str(Path(__file__).parent.parent.parent / Path("workspace") / Path("gpt-pilot-test"))

