from unittest.mock import patch
import pytest
from tempfile import TemporaryDirectory

from utils.ignore import IgnoreMatcher  # Import IgnoreMatcher class from utils.ignore module

@pytest.mark.parametrize(
    ("path", "expected"),
    [
        (".git", True),
        (".gpt-pilot", True),
        (".idea", True),
        (".vscode", True),
        (".DS_Store", True),
        (join("subdirectory", ".DS_Store"), True),
        ("__pycache__", True),
        (join("subdirectory", "__pycache__"), True),
        ("node_modules", True),
        (join("subdirectory", "node_modules"), True),
        ("package-lock.json", True),
        ("venv", True),
        ("dist", True),
        ("build", True),
        ("target", True),
        (".gitignore", False),
        ("server.js", False),
        (join(dirname(__file__), "node_modules"), True),
        (join(dirname(__file__), "subdirectory", "node_modules"), True),
    ]
)
@patch("utils.ignore.os.path.getsize")
@patch("utils.ignore.os.path.isfile")
@patch("utils.ignore.open")
def test_default_ignore(mock_open, mock_isfile, mock_getsize, path, expected):
    # Test the default ignore functionality of IgnoreMatcher class
    mock_open.return_value.read.return_value = "fake-content"
    mock_isfile.return_value = True
    mock_getsize.return_value = 100
    matcher = IgnoreMatcher(root_path=dirname(__file__))  # Initialize IgnoreMatcher instance
    assert matcher.ignore(path) == expected  # Check if the given path should be ignored


@pytest.mark.parametrize(
    ("ignore", "path", "expected"),
    [
        ("*.py[co]", "test.pyc", True),
        ("*.py[co]", "subdir/test.pyo", True),
        ("*.py[co]", "test.py", False),
        ("*.min.js", f"public{sep}js{sep}script.min.js", True),
        ("*.min.js", f"public{sep}js{sep}min.js", False),
    ]
)
@patch("utils.ignore.os.path.getsize")
@patch("utils.ignore.os.path.isfile")
@patch("utils.ignore.open")
def test_additional_ignore(mock_open, mock_isfile, mock_getsize, ignore, path, expected):
    # Test the additional ignore functionality of IgnoreMatcher class
    mock_open.return_value.read.return_value = "fake-content"
    mock_isfile.return_value = True
    mock_getsize.return_value = 100
    matcher = IgnoreMatcher([ignore])  # Initialize IgnoreMatcher instance with a list of ignore patterns
    assert matcher.ignore(path) == expected  # Check if the given path should be ignored


@pytest.mark.parametrize(
    ("ignore", "path", "expected"),
    [
        ("jquery.js", "jquery.js", True),
        ("jquery.js", f"otherdir{sep}jquery.js", True),
        ("jquery.js", f"{sep}test{sep}jquery.js", True),
    ]
)
def test_full_path(ignore, path, expected):
    # Test the full path ignore functionality of IgnoreMatcher class
    matcher = IgnoreMatcher([ignore], root_path=f"{sep}test")  # Initialize IgnoreMatcher instance with a root path
    assert matcher.ignore(path) == expected  # Check if the given path should be ignored


@pytest.mark.parametrize(
    ("size", "expected"),
    [
        (1024*1024, True),  # 1MB
        (49999, False),    # one byte less than the threshold
    ]
)
@patch("utils.ignore.os.path.isfile")
@patch("utils.ignore.os.path.getsize")
def test_ignore_large_files(mock_getsize, mock_isfile, size, expected):
    # Test the large file ignore functionality of IgnoreMatcher class
    mock_isfile.return_value = True
    mock_getsize.return_value = size
    matcher = IgnoreMatcher(root_path=f"{sep}test")  # Initialize IgnoreMatcher instance

    with patch.object(matcher, "is_binary", return_value=False):
        # Patch the is_binary method to return False
        assert matcher.ignore("fakefile.txt") is expected

    mock_isfile.assert_called_once()
    mock_getsize.assert_called_once_with(f"{sep}test{sep}fakefile.txt")


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        (("hello world ŠĐŽČĆ").encode("utf-8"), False),  # text
        (b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52", True), # image
    ]
)
def test_ignore_binary_files(content, expected):
    # Test the binary file ignore functionality of IgnoreMatcher class
    with TemporaryDirectory() as tmpdir:
        path = join(tmpdir, "testfile.txt")
        with open(path, "wb") as fp:
            fp.write(content)

        matcher = IgnoreMatcher(root_path=tmpdir)
        # Check both relative and absolute paths
        assert matcher.ignore("testfile.txt") is expected
        assert matcher.ignore(path) is expected

@patch("utils.ignore.os.path.is
