import pathlib
from glob import glob
from typing import List, Optional

from const.common import IGNORE_PATHS, IGNORE_SIZE_THRESHOLD


class IgnoreMatcher:
    def __init__(
        self,
        ignore_paths: Optional[List[str]] = None,
        root_path: Optional[str] = None,
        ignore_binaries: bool = True,
        ignore_large_files: bool = True,
    ):
        """
        Initialize the IgnoreMatcher object.

        The passed paths (optional) are added to the list of ignore paths
        from `const.common.IGNORE_PATHS`.

        :param ignore_paths: List of paths to ignore (optional)
        :param root_path: The root path for relative paths
        :param ignore_binaries: Whether to ignore binary files
        :param ignore_large_files: Whether to ignore files larger than the threshold
        """
        if ignore_paths is None:
            ignore_paths = []

        self.ignore_paths = ignore_paths + IGNORE_PATHS
        self.ignore_binaries = ignore_binaries
        self.ignore_large_files = ignore_large_files
        self.root_path = root_path

    def __str__(self):
        return (
            f"IgnoreMatcher(ignore_paths={self.ignore_paths}, "
            f"root_path={self.root_path}, "
            f"ignore_binaries={self.ignore_binaries}, "
            f"ignore_large_files={self.ignore_large_files})"
        )

    def __repr__(self):
        return self.__str__()

    def ignore(self, path: str) -> bool:
        """
        Check if the given path matches any of the ignore patterns.

        :param path: Path to the file or directory to check
        :return: True if the path matches any of the ignore patterns, False otherwise
        """
        path = pathlib.Path(path)

        if self.root_path:
            path = self.root_path / path

        return (
            self.is_in_ignore_list(path)
            or self.is_large_file(path)
            if self.ignore_large_files
            else False
            or self.is_binary(path) if self.ignore_binaries else False
        )

    def is_in_ignore_list(self, path: pathlib.Path) -> bool:
        """
        Check if the given path matches any of the ignore patterns.

        :param path: The path to the file or directory to check
        :return: True if the path matches any of the ignore patterns, False otherwise.
        """
        name = path.name
        return any(path.match(pattern) for pattern in self.ignore_paths)

    def is_large_file(self, path: pathlib.Path) -> bool:
        """
        Check if the given file is larger than the threshold.

        This also returns True for files that aren't accessible, since
        we want to ignore those as well.

        :param path: FULL path to the file to check.
        :return: True if the file is larger than the threshold, False otherwise.
        """
        return path.stat().st_size > IGNORE_SIZE_THRESHOLD if path.is_file() else False

    def is_binary(self, path: pathlib.Path) -> bool:
        """
        Check if the given file is binary and should be ignored.

        This also returns True if the file doesn't exist or can't be opened,
        since we want to ignore those kinds of files as well.

        :param path: FULL path to the file to check.
        :return: True if the file should be ignored, False otherwise.
        """
        try:
            with path.open("rb") as file:
                first_byte = file.read(1)
            return first_byte.is_binary()
        except OSError:
            return True
