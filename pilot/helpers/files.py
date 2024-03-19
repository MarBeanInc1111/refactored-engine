from pathlib import Path
import os
from typing import Optional, Union, List, Dict

from utils.style import color_green
from utils.ignore import IgnoreMatcher

def update_file(path: str, new_content: Union[str, bytes], project: Optional[object] = None):
    """
    Update the content of a file at the given path.

    :param path: The full path to the file to update.
    :param new_content: The new content to write to the file. This can be a string or bytes object.
    :param project: An optional Project object related to the file update. Default is None.

    This function creates any necessary intermediate directories before writing to the file.
    If the file is a text file, it will be written using UTF-8 encoding.

    If the 'project' parameter is not None, the function prints a message indicating that the file has been updated,
    but only if 'skip_steps' is False and 'check_ipc()' returns True.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)

    if isinstance(new_content, str):
        file_mode = "w"
        encoding = "utf-8"
    else:
        file_mode = "wb"
        encoding = None

    with open(path, file_mode, encoding=encoding) as file:
        file.write(new_content)

        if project is not None and not project.skip_steps and project.check_ipc():
            print(color_green(f"Updated file {path}"))

def get_file_contents(path: str, project_root_path: str) -> Dict[str, Union[str, bytes]]:
    """
    Get the content and metadata of a file at the given path.

    :param path: The full path to the file.
    :param project_root_path: The full path to the project root directory.
    :return: A dictionary containing the following keys:
        - 'name': The name of the file.
        - 'path': The relative path to the file.
        - 'content': The content of the file as a string or bytes object.
        - 'full_path': The full path to the file.
        - 'lines_of_code': The number of lines in the file.

    This function reads the file as a text file using UTF-8 encoding. If that fails, it reads the file as a binary file.
    """
    full_path = Path(path).resolve().absolute()

    try:
        if full_path.is_file():
            with open(full_path, "r", encoding="utf-8") as file:
                file_content = file.read()
        else:
            raise ValueError(f"Path is not a file: {path}")

    except UnicodeDecodeError:
        with open(full_path, "rb") as file:
            file_content = file.read()

    except (NotADirectoryError, FileNotFoundError):
        raise ValueError(f"Path is not a directory or file not found: {path}")

    except Exception as e:
        raise ValueError(f"Exception in get_file_contents: {e}")

    file_name = full_path.name
    relative_path = str(full_path.relative_to(project_root_path))

    if relative_path == '.':
        relative_path = ''

    return {
        "name": file_name,
        "path": relative_path,
        "content": file_content,
        "full_path": str(full_path),
        "lines_of_code": len(file_content.splitlines()),
    }

def get_directory_contents(directory: str, ignore: Optional[List[str]] = None) -> List[Dict[str, Union[str, bytes]]]:
    """
    Get the content of all files in the given directory.

    :param directory: The full path to the directory.
    :param ignore: An optional list of files or folders to ignore. Default is None.
    :return: A list of dictionaries containing the content and metadata of each file.

    See `get_file_contents()` for the details on the output structure
    and how files are read.
    """
    return_array = []

    matcher = IgnoreMatcher(ignore, root_path=directory)

    for dpath, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not matcher.ignore(os.path.join(dpath, d))]

        for file in files:
            full_path = os.path.join(dpath, file)

            if matcher.ignore(full_path):
                continue

            return_array.append(get_file_contents(full_path, directory))

    return return_array

def clear_directory(directory: str, ignore: Optional[List[str]] = None):
    """
    Clear the content of a directory by removing all files and
    subdirectories.

    :param directory: The full path to the directory.
    :param ignore: An optional list of files or folders to ignore. Default is None.
    """
    matcher = IgnoreMatcher(ignore, root_path=directory)

    for dpath, dirs, files in os.walk(directory, topdown=False):
        dirs[:] = [d for d in dirs if not matcher.ignore(os.path.join(dpath, d))]

        for file in files:
            full_path = os.path.join(dpath, file)

            if matcher.ignore(full_path):
                continue

            if os.path.isfile(full_path):
                os.remove(full_path)
            elif os.path.is
