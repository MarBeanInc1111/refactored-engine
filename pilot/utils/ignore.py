from fnmatch import fnmatch
import os.path
from typing import Optional

from const.common import IGNORE_PATHS, IGNORE_SIZE_THRESHOLD


class IgnoreMatcher:
    def __init__(self,
        ignore_paths: Optional[list[str]] = None,
        *,
        root_path: Optional[None] = None,
        ignore_binaries: bool = True,
        ignore_large_files: bool = True,
    ):
        """
        Initialize the IgnoreMatcher object.

        The passed paths (optional) are *added* to the list of
        ignore paths from `const.common.IGNORE_PATHS`.

        :param ignore_paths: List of paths to ignore (optional)
        """
        if ignore_paths is None:
            ignore_paths = []

        # The list of ignore paths is a combination of the provided paths and the
        # default ignore paths from the `const.common` module
        self.ignore_paths = ignore_paths + IGNORE_PATHS
        self.ignore_binaries = ignore_binaries
        self.ignore_large_files = ignore_large_files
        self.root_path = root_path

    def ignore(self, path: str) -> bool:
        """
        Check if the given path matches any of the ignore patterns.

        Specified path can be either the full path, or a relative path
        (if root_path was set in the constructor).

        :param path: Path to the file or directory to check
        :return: True if the path matches any of the ignore patterns, False otherwise
        """

        # Turn into absolute (full) path
        if self.root_path and not path.startswith(self.root_path):
            path = os.path.join(self.root_path, path)

        # Check if the path is in the ignore list
        if self.is_in_ignore_list(path):
            return True

        # Check if the file is larger than the threshold
        if self.ignore_large_files and self.is_large_file(path):
            return True

        # Check if the file is binary
        if self.ignore_binaries and self.is_binary(path):
            return True

        return False

    def is_in_ignore_list(self, path: str) -> bool:
        """
        Check if the given path matches any of the ignore patterns.

        :param path: The path to the file or directory to check
        :return: True if the path matches any of the ignore patterns, False otherwise.
        """
        name = os.path.basename(path)
        for pattern in self.ignore_paths:
            if fnmatch(name, pattern):
                return True
        return False

    def is_large_file(self, path: str) -> bool:
        """
        Check if the given file is larger than the threshold.

        This also returns True for files that aren't accessible, since
        we want to ignore those as well.

        :param path: FULL path to the file to check.
        :return: True if the file is larger than the threshold, False otherwise.
        """
        # Check if the path is a valid file
        if not os.path.isfile(path):
            return False

        try:
            # Check if the file size is larger than the threshold
            file_size = os.path.getsize(path)
            return file_size > IGNORE_SIZE_THRESHOLD
        except:  # noqa
            # If there is an error while getting the file size, return True
            # to ignore the file
            return True

    def is_binary(self, path: str) -> bool:
        """
        Check if the given file is binary and should be ignored.

        This also returns True if the file doesn't exist or can't be opened,
        since we want to ignore those kinds of files as well.

        :param path: FULL path to the file to check.
        :return: True if the file should be ignored, False otherwise.
        """
        # Check if the path is a valid file
        if not os.path.isfile(path):
            return False

        try:
            # Open the file and try to read it as a text file
            with open(path, "r", encoding="utf-8") as file:
                file.read(128*1024)
            # If the file can be read as a text file, return False
            return False
        except:  # noqa
            # If there is an error while opening or reading the file,
            # return True to ignore the file
            return True
