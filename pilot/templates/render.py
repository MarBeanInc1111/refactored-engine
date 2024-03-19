from __future__ import annotations

import os
import os.path
from typing import Any, Callable

import jinja2


class Renderer:
    """
    Render Jinja templates using a given context.

    This class sets up a Jinja renderer and provides methods to render one or
    more templates using a provided context. The rendered templates are returned
    as strings, and nothing is written to disk.

    Attributes:
        template_dir (str): The directory where the templates are located.
        jinja_env (jinja2.Environment): The Jinja environment used for rendering.
    """

    def __init__(self, template_dir: str):
        """
        Initialize the Renderer object.

        Args:
            template_dir (str): The directory where the templates are located.
        """
        self.template_dir = template_dir
        self.jinja_env = self._create_jinja_environment()

    def _create_jinja_environment(self) -> jinja2.Environment:
        """
        Create and configure the Jinja environment.

        Returns:
            jinja2.Environment: The Jinja environment used for rendering.
        """
        return jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_dir),
            autoescape=False,
            lstrip_blocks=True,
            trim_blocks=True,
            keep_trailing_newline=True,
        )

    def render_template(self, template: str, context: Any) -> str:
        """
        Render a single template to a string using the provided context.

        Args:
            template (str): The name of the template file, relative to the
                template directory.
            context (Any): The context used for rendering the template.

        Returns:
            str: The rendered template as a string.
        """
        template = template.replace('\\', '/')  # Jinja2 uses '/' on all platforms

        tpl_object = self.jinja_env.get_template(template)
        return tpl_object.render(context)

    def render_tree(
        self, root: str, context: Any, filter_func: Callable[[str], str | None] | None = None
    ) -> dict[str, str]:
        """
        Render a tree of templates using the provided context.

        Args:
            root (str): The root of the tree (relative to the template directory).
            context (Any): The context used for rendering the templates.
            filter_func (Callable[[str]], str | None): A function to filter the files to render.
                If provided, it should take a single string argument (the file
                path relative to the tree root) and return a string (the
                output file path) or None (to skip the file).

        Returns:
            dict[str, str]: A dictionary containing the rendered templates,
                with file paths as keys and the rendered content as values.
        """
        rendered_templates = {}
        full_root = os.path.join(self.template_dir, root)

        for path, subdirs, files in os.walk(full_root):
            for file in files:
                file_path = os.path.join(path, file)  # Full path of the template file
                tpl_location = os.path.relpath(file_path, self.template_dir)  # Template location relative to template_dir
                output_location = os.path.relpath(file_path, full_root)  # Template location relative to tree root

                if filter_func and filter_func(output_location) is None:
                    continue

                contents = self.render_template(tpl_location, context)
                rendered_templates[output_location] = contents

        return rendered_templates
