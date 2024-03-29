import os
from typing import Dict, List, Optional
from uuid import uuid4

from utils.style import color_green_bold
from logger.logger import logger
from utils.exit import trace_code_event

from .node_express_mongoose import NODE_EXPRESS_MONGOOSE
from .render import Renderer

PROJECT_TEMPLATES = {
    "node_express_mongoose": NODE_EXPRESS_MONGOOSE,
}

def render_and_save_files(
    template: Dict,
    project_name: str,
    project_description: str,
    root_path: str,
    random_secret: str,
) -> List[Dict]:
    r = Renderer(os.path.join(os.path.dirname(__file__), "tpl"))
    files = r.render_tree(template["path"], {
        "project_name": project_name,
        "project_description": project_description,
        "random_secret": random_secret,
    })

    project_files = []

    for file_name, file_content in files.items():
        full_path = os.path.join(root_path, file_name)
        if not os.path.exists(os.path.dirname(full_path)):
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(file_content)
        except Exception as err:
            logger.error(f"Error saving file '{file_name}': {err}", exc_info=True)

        rel_dir = os.path.dirname(file_name)
        project_files.append({
            "name": os.path.basename(file_name),
            "path": "/" if rel_dir in ["", "."] else rel_dir,
            "content": file_content,
        })

    return project_files

def apply_project_template(
    project: "Project",
) -> Optional[str]:
    """
    Apply a project template to a new project.

    :param project: the project object
    :return: a summary of the applied template, or None if no template was applied
    """
    template_name = project.project_template
    if not template_name or template_name not in PROJECT_TEMPLATES:
        logger.warning(f"Project template '{template_name}' not found, ignoring")
        return None

    root_path = project.root_path
    project_name = project.args['name']
    project_description = project.main_prompt
    template = PROJECT_TEMPLATES[template_name]
    install_hook = template.get("install_hook")

    random_secret = uuid4().hex

    project_files = render_and_save_files(
        template,
        project_name,
        project_description,
        root_path,
        random_secret,

