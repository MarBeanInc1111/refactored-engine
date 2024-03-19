import sys
import time
from typing import Any
from uuid import uuid4

import requests
from logging import getLogger
from pathlib import Path
from typing import Dict, Optional

# Add your import statements here

class Telemetry:
    DEFAULT_ENDPOINT = "https://api.pythagora.io/telemetry"
    MAX_CRASH_FRAMES = 3

    def __init__(self):
        self.enabled = False
        self.telemetry_id = None
        self.endpoint = None
        self.clear_data()

        self._initialize_from_settings()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Telemetry, cls).__new__(cls)
        return cls._instance

    def _initialize_from_settings(self):
        if settings.telemetry is not None:
            self.enabled = settings.telemetry.get("enabled", False)
            self.telemetry_id = settings.telemetry.get("id")
            self.endpoint = settings.telemetry.get("endpoint")

        if self.enabled:
            log.debug(
                f"Anonymous telemetry enabled (id={self.telemetry_id}), "
                f"configure or disable it in {config_path}"
            )

    def clear_data(self, telemetry_data: Optional[Dict[str, Any]] = None):
        """
        Reset all telemetry data to default values.
        """
        self.data = {
            # System platform
            "platform": sys.platform,
            # Python version used for GPT Pilot
            "python_version": sys.version,
            # GPT Pilot version
            "pilot_version": version,
            # GPT Pilot Extension version
            "extension_version": None,
            # Is extension used
            "is_extension": False,
            # LLM used
            "model": None,
            # Initial prompt
            "initial_prompt": None,
            # Optional user contact email
            "user_contact": None,
            # Unique project ID (app_id)
            "app_id": None,
            # Project architecture
            "architecture": None,
        }
        if sys.platform == "linux":
            try:
                import distro
                self.data["linux_distro"] = distro.name(pretty=True)
            except Exception as err:
                log.debug(f"Error getting Linux distribution info: {err}", exc_info=True)
        self.clear_counters()

        if telemetry_data:
            self.data.update(telemetry_data)

    def clear_counters(self):
        """
        Reset telemetry counters while keeping the base data.
        """
        self.data.update({
            # Number of LLM requests made
            "num_llm_requests": 0,
            # Number of LLM requests that resulted in an error
            "num_llm_errors": 0,
            # Number of tokens used for LLM requests
            "num_llm_tokens": 0,
            # Number of development steps
            "num_steps": 0,
            # Number of commands run during development
            "num_commands": 0,
            # Number of times a human input was required during development
            "num_inputs": 0,
            # Number of files in the project
            "num_files": 0,
            # Total number of lines in the project
            "num_lines": 0,
            # Number of tasks started during development
            "num_tasks": 0,
            # Number of seconds elapsed during development
            "elapsed_time": 0,
            # Total number of lines created by GPT Pilot
            "created_lines": 0,
            # End result of development:
            # - success:initial-project
            # - success:feature
            # - success:exit
            # - failure
            # - failure:api-error
            # - interrupt
            "end_result": None,
            # Whether the project is continuation of a previous session
            "is_continuation": False,
            # Optional user feedback
            "user_feedback": None,
            # If GPT Pilot crashes, record diagnostics
            "crash_diagnostics": None,
            # Statistics for large requests
            "large_requests": None,
            # Statistics for slow requests
            "slow_requests": None,
        })
        self.start_time = None
        self.end_time = None
        self.large_requests = []
        self.slow_requests = []

    def record(self, name: str, value: Any):
        """
        Record a telemetry event.

        :param name: name of the telemetry event
        :param value: value to record

        Note: only known data fields may be recorded, see `Telemetry.clear_data()` for a list.
        """
        if name not in self.data:
            log.error(
                f"Telemetry.record(): ignoring unknown telemetry data field: {name}"
            )
            return

        if isinstance(value, int):
            self.data[name] += value
        else:
            self.data[name] = value

    def start(self):
        """
        Record start of application creation process.
        """
        self.
