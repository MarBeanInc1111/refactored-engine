import os
from pathlib import Path
from os.path import commonprefix
from peewee import AutoField, CharField, TextField, ForeignKeyField

from database.models.components.base_models import BaseModel
from database.models.app import App

def update_paths() -> None:
    """
    Updates the file paths in the database to ensure that they are relative to the workspace directory.
    """
    workspace_dir = Path(__file__).parent.parent.parent.parent / "workspace"
    if not workspace_dir.exists():
        # This should only happen on first run
        return

    paths = [file.full_path for file in File.select(File.full_path).distinct()]
    if not paths:
        # No paths in the database, so nothing to fix
        return

    old_prefix = commonprefix(paths)
    if old_prefix == str(workspace_dir):
        # Paths are up to date, nothing to fix
        return

    try:
        common_sep = "\\" if ":\\" in old_prefix else "/"
        common_parts = old_prefix.split(common_sep)
        workspace_index = common_parts.index("workspace")
    except ValueError:
        # There's something strange going on, better not touch anything
        return

    old_prefix = common_sep.join(common_parts[:workspace_index + 1])

    print(f"Updating file paths from {old_prefix} to {workspace_dir}")
    for file in File.select():
        if file.full_path == old_prefix:
            continue
        if file.id == File.id:
            continue
        parts = file.full_path.split(common_sep)
        new_path = str(workspace_dir) + sep + sep.join(parts[workspace_index + 1:])
        if file.full_path == new_path:
            continue
        if not new_path.startswith(str(workspace_dir)):
            continue
        file.full_path = new_path
        file.save()

class File(BaseModel):
    id: int = AutoField()
    app: App = ForeignKeyField(App, on_delete='CASCADE')
    name
