import os.path
import re
from typing import Dict, List, Optional, Tuple
from traceback import format_exc
from difflib import unified_diff

from helpers.AgentConvo import AgentConvo
from helpers.Agent import Agent
from helpers.files import get_file_contents
from const.function_calls import GET_FILE_TO_MODIFY, REVIEW_CHANGES
from logger.logger import logger

# Constant for indicating missing new line at the end of a file in a unified diff
NO_EOL = "\ No newline at end of file"

# Regular expression pattern for matching hunk headers
PATCH_HEADER_PATTERN = re.compile(r"^@@ -(\d+),?(\d+)? \+(\d+),?(\d+)? @@")

MAX_REVIEW_RETRIES = 3

class CodeMonkey(Agent):
    """
    A helper class that implements code changes described in a given
    code_changes_description.
    """
    save_dev_steps: bool

    def __init__(self, project):
        super().__init__('code_monkey', project)

    def get_original_file(
            self,
            code_changes_description: str,
            step: Dict[str, str],
            files: List[Dict]
    ) -> Tuple[str, str]:
        """
        Get the original file content and name.

        :param code_changes_description: description of the code changes
        :param step: information about the step being implemented
        :param files: list of files to send to the LLM
        :return: tuple of (file_name, file_content)
        """
        if 'path' not in step or 'name' not in step:
            file_to_change = self.identify_file_to_change(code_changes_description, files)
            step['path'] = os.path.dirname(file_to_change)
            step['name'] = os.path.basename(file_to_change)

        rel_path, abs_path = self.project.get_full_file_path(step['path'], step['name'])

        for f in files:
            if (f['path'] == step['path'] or (os.path.sep + f['path'] == step['path'])) and f['name'] == step['name'] and f['content']:
                file_content = f['content']
                break
        else:
            try:
                file_content = get_file_contents(abs_path, self.project.root_path)['content']
                if isinstance(file_content, bytes):
                    file_content = "... <binary file, content omitted> ..."
            except ValueError:
                file_content = ""

        file_name = os.path.join(rel_path, step['name'])
        return file_name, file_content

    def implement_code_changes(
            self,
            convo: Optional[AgentConvo],
            step: Dict[str, str]
    ) -> AgentConvo:
        """
        Implement code changes described in `code_changes_description`.

        :param convo: conversation to continue (must contain file coding/modification instructions)
        :param step: information about the step being implemented
        """
        code_change_description = step.get('code_change_description')

        files = self.project.get_all_coded_files()
        file_name, file_content = self.get_original_file(code_change_description, step, files)

        print('', type='verbose', category='agent:code-monkey')

        if file_content:
            print(f'Updating existing file {file_name}:')
        else:
            print(f'Creating new file {file_name}:')

        # Get the new version of the file
        content = self.replace_complete_file(
            convo,
            file_content,
            file_name,
            files,
        )

        for i in range(MAX_REVIEW_RETRIES):
            if not content or content == file_content:
                # There are no changes or there was problem talking with the LLM, we're done here
                break

            print('Sending code for review...', type='verbose', category='agent:code-monkey')
            print('', type='verbose', category='agent:reviewer')
            content, rework_feedback = self.review_change(convo, code_change_description, file_name, file_content, content)
            print('Review finished. Continuing...', type='verbose', category='agent:code-monkey')
            if not rework_feedback:
                # No rework needed, we're done here
                break

            print('', type='verbose', category='agent:code-monkey')
            content = convo.send_message('development/review_feedback.prompt', {
                "content": content,
                "original_content": file_content,
                "rework_feedback": rework_feedback,
            })
            if content:
                content = self.remove_backticks(content)

        # If we have changes, update the file
        if content and content != file_content:
            if not self.project.skip_steps:
                delta_lines = len(content.splitlines()) - len(file_content.splitlines())
                telemetry.inc("created_lines", delta_lines)
            self.project.save_file({
                'path': step['path'],
                'name': step['name'],
                'content': content,
            })

        return convo

    def replace_complete_file(
            self,
            convo: AgentConvo,
            file_content: str,
            file_name: str,
            files: List[Dict]
    ) -> str:
        """
        As a fallback, replace the complete file content.

        This should only be used if we've failed to replace individual code blocks.

        :param convo: AgentConvo instance
