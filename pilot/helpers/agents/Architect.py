import json
from typing import Dict, List, Any
import platform

import warnings

from utils.utils import step_already_finished, should_execute_step, generate_app_data
from database.database import save_progress, get_progress_steps
from logger.logger import logger
from helpers.AgentConvo import AgentConvo
from prompts.prompts import ask_user
from templates import PROJECT_TEMPLATES

ARCHITECTURE_STEP = 'architecture'
SYSTEM_DEP_WARNINGS = ["docker", "kubernetes", "microservices"]
FRAMEWORK_WARNINGS = ["react", "react.js", "next.js", "vue", "vue.js", "svelte", "angular"]
FRAMEWORK_WARNINGS_URL = "https://github.com/Pythagora-io/gpt-pilot/wiki/Using-GPT-Pilot-with-frontend-frameworks"

class Architect:
    def __init__(self, project):
        self.project = project
        self.convo_architecture = None

    def get_architecture(self) -> None:
        """
        Plans the project architecture and saves it to the database.
        """
        project_stage_data = {
            "project_stage": "architecture"
        }
        print(json.dumps(project_stage_data), type='info')

        self.project.current_step = ARCHITECTURE_STEP

        step = get_progress_steps(self.project.args['app_id'], ARCHITECTURE_STEP)
        if step and not should_execute_step(self.project.args['step'], ARCHITECTURE_STEP):
            step_already_finished(self.project.args, step)
            self._load_db_data(step)
            return

        print(f"Planning project architecture...\n")
        logger.info("Planning project architecture...")

        self.convo_architecture = AgentConvo(self)
        try:
            llm_response = self.convo_architecture.send_message('architecture/technologies.prompt',
                {'name': self.project.args['name'],
                 'app_summary': self.project.project_description,
                 'user_stories': self.project.user_stories,
                 'user_tasks': self.project.user_tasks,
                 "os": platform.system(),
                 'app_type': self.project.args['app_type'],
                 "templates": PROJECT_TEMPLATES,
                },
                ARCHITECTURE_STEP
            )
        except Exception as e:
            print(f"Error while generating architecture: {e}", type='error')
            return

        self._update_project_data(llm_response)

        self._check_warnings()

        logger.info(f"Final architecture: {self.project.architecture}")

        save_progress(self.project.args['app_id'], self.project.current_step, {
            "messages": self.convo_architecture.messages,
            "architecture": llm_response,
            "app_data": generate_app_data(self.project.args)
        })

        return

    def _load_db_data(self, step: Dict[str, Any]) -> None:
        """
        Loads data from the database if the step has already been executed.
        """
        db_data = step.get("architecture", {})
        if db_data:
            self.project.architecture = db_data.get("architecture", "")
            self.project.system_dependencies = db_data.get("system_dependencies", [])
            self.project.package_dependencies = db_data.get("package_dependencies", [])
            self.project.project_template = db_data.get("project_template", None)

    def _update_project_data(self, llm_response: Dict[str, Any]) -> None:
        """
        Updates the project data with the generated architecture.
        """
        self.project.architecture = llm_response["architecture"]
        self.project.system_dependencies = llm_response["system_dependencies"]
        self.project.package_dependencies = llm_response["package_dependencies"]
        self.project.project_template = llm_response["template"]

    def _check_warnings(self) -> None:
        """
        Checks for warnings and displays them to the user.
        """
        warn_system_deps = [dep["name"] for dep in self.project.system_dependencies if dep["name"].lower() in SYSTEM_DEP_WARNINGS]
        warn_package_deps = [dep["name"] for dep in self.project.package_dependencies if dep["name"].lower() in FRAMEWORK_WARNINGS]

        if warn_system_deps:
            warnings.warn("The following system dependencies were detected and might require additional configuration: " +
                          ", ".join(warn_system_deps), UserWarning)

        if warn_package_deps:
            warnings.warn("The following frontend frameworks were detected. "
                          "Please follow the instructions in the documentation to properly set up the project: " +
                          FRAMEWORK_WARNINGS_URL, UserWarning)
