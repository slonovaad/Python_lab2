import unittest
import os.path
from unittest.mock import patch
from src.commands.cd import cd


class CdTestCase(unittest.TestCase):
    """Тесты для команы cd"""

    def test_dont_have_paths(self):
        with (patch("src.commands.cd.invalid_arguments_error_message") as mock_error,
              patch("os.chdir") as mock_chdir):
            cd([], [])
            mock_chdir.assert_not_called()
            mock_error.assert_called_once_with("cd")

    def test_have_options(self):
        with (patch("src.commands.cd.invalid_arguments_error_message") as mock_error,
              patch("os.chdir") as mock_chdir):
            cd(["-r"], ["directory_path"])
            mock_chdir.assert_not_called()
            mock_error.assert_called_once_with("cd")

    def test_have_more_than_one_path(self):
        with (patch("src.commands.cd.invalid_arguments_error_message") as mock_error,
              patch("os.chdir") as mock_chdir):
            cd([], ["directory1_path", "directory2_path"])
            mock_chdir.assert_not_called()
            mock_error.assert_called_once_with("cd")

    def test_correct_path(self):
        with (patch("os.chdir") as mock_chdir,
              patch("logging.info") as mock_log):
            cd([], ["directory_path"])
            mock_chdir.assert_called_once_with(os.path.abspath("directory_path"))
            mock_log.assert_called_once_with("Success")

    def test_correct_abspath(self):
        with (patch("os.chdir") as mock_chdir,
              patch("logging.info") as mock_log):
            cd([], [os.path.abspath("directory_path")])
            mock_chdir.assert_called_once_with(os.path.abspath("directory_path"))
            mock_log.assert_called_once_with("Success")

    def test_homedir(self):
        with (patch("os.chdir") as mock_chdir,
              patch("logging.info") as mock_log):
            cd([], ["~"])
            mock_chdir.assert_called_once_with(os.path.expanduser("~"))
            mock_log.assert_called_once_with("Success")

    def test_not_exist(self):
        with (patch("src.commands.cd.not_exist_error_message") as mock_error,
              patch("os.chdir") as mock_chdir):
            mock_chdir.side_effect = FileNotFoundError
            cd([], ["directory_path"])
            mock_chdir.assert_called_once_with(os.path.abspath("directory_path"))
            mock_error.assert_called_once_with("cd", "directory", "directory_path")

    def test_not_allowed(self):
        with (patch("src.commands.cd.access_error_message") as mock_error,
              patch("os.chdir") as mock_chdir):
            mock_chdir.side_effect = PermissionError
            cd([], ["directory_path"])
            mock_chdir.assert_called_once_with(os.path.abspath("directory_path"))
            mock_error.assert_called_once_with("cd", "directory", "directory_path")

    def test_not_a_directory(self):
        with (patch("src.commands.cd.wrong_type_error_message") as mock_error,
              patch("os.chdir") as mock_chdir):
            mock_chdir.side_effect = NotADirectoryError
            cd([], ["file_path"])
            mock_chdir.assert_called_once_with(os.path.abspath("file_path"))
            mock_error.assert_called_once_with("cd", "directory", "file_path")
