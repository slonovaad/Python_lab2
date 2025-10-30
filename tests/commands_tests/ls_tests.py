import unittest
import os
from unittest.mock import patch
from src.commands.ls import ls


class LsTestCase(unittest.TestCase):
    """Тесты для команы ls"""

    def test_more_than_one_paths(self):
        with (patch("src.commands.ls.invalid_arguments_error_message") as mock_error,
              patch("src.commands.ls.open") as mock_open):
            ls([], ["dir1", "dir2"])
            mock_open.assert_not_called()
            mock_error.assert_called_once_with("ls")

    def test_current_dir(self):
        with (patch("logging.info") as mock_log,
              patch("os.listdir") as mock_listdir,
              patch("src.commands.ls.print_data") as mock_print_data):
            mock_listdir.return_value = ["file1", "file2"]
            ls([], [])
            mock_listdir.assert_called_once()
            mock_print_data.assert_called_once_with(["file1", "file2"])
            mock_log.assert_called_once_with("Success")

    def test_current_dir_not_allowed(self):
        with (patch("src.commands.ls.access_error_message") as mock_error,
              patch("os.listdir") as mock_listdir,
              patch("src.commands.ls.print_data") as mock_print_data):
            mock_listdir.side_effect = PermissionError
            ls([], [])
            mock_listdir.assert_called_once()
            mock_print_data.assert_not_called()
            mock_error.assert_called_once_with("ls", "directory", os.getcwd())

    def test_current_dir_more_one_option(self):
        with (patch("src.commands.ls.invalid_arguments_error_message") as mock_error,
              patch("os.listdir") as mock_listdir,
              patch("src.commands.ls.print_data") as mock_print_data):
            ls(["-l", "-r"], [])
            mock_listdir.assert_not_called()
            mock_print_data.assert_not_called()
            mock_error.assert_called_once_with("ls")

    def test_current_dir_wrong_option(self):
        with (patch("src.commands.ls.invalid_option_error_message") as mock_error,
              patch("os.listdir") as mock_listdir,
              patch("src.commands.ls.print_data") as mock_print_data):
            ls(["-r"], [])
            mock_listdir.assert_not_called()
            mock_print_data.assert_not_called()
            mock_error.assert_called_once_with("ls", "-r")

    def test_current_dir_details(self):
        with (patch("logging.info") as mock_log,
              patch("os.listdir") as mock_listdir,
              patch("src.commands.ls.print_data") as mock_print_data):
            mock_listdir.return_value = ["file1", "file2"]
            ls(["-l"], [])
            mock_listdir.assert_called_once()
            mock_print_data.assert_called_once_with(["file1", "file2"], details=True)
            mock_log.assert_called_once_with("Success")

    def test_current_dir_detais_not_allowed(self):
        with (patch("src.commands.ls.access_error_message") as mock_error,
              patch("os.listdir") as mock_listdir,
              patch("src.commands.ls.print_data") as mock_print_data):
            mock_listdir.side_effect = PermissionError
            ls(["-l"], [])
            mock_listdir.assert_called_once()
            mock_print_data.assert_not_called()
            mock_error.assert_called_once_with("ls", "directory", os.getcwd())

    def test_given_dir(self):
        with (patch("logging.info") as mock_log,
              patch("os.listdir") as mock_listdir,
              patch("src.commands.ls.print_data") as mock_print_data):
            mock_listdir.return_value = ["file1", "file2"]
            ls([], ["dir"])
            mock_listdir.assert_called_once_with(os.path.abspath("dir"))
            mock_print_data.assert_called_once_with([
                os.path.join(os.path.abspath("dir"), "file1"),
                os.path.join(os.path.abspath("dir"), "file2")])
            mock_log.assert_called_once_with("Success")

    def test_given_home_dir(self):
        with (patch("logging.info") as mock_log,
              patch("os.listdir") as mock_listdir,
              patch("src.commands.ls.print_data") as mock_print_data):
            mock_listdir.return_value = ["file1", "file2"]
            ls([], ["~"])
            mock_listdir.assert_called_once_with(os.path.expanduser("~"))
            mock_print_data.assert_called_once_with([
                os.path.join(os.path.expanduser("~"), "file1"),
                os.path.join(os.path.expanduser("~"), "file2")])
            mock_log.assert_called_once_with("Success")

    def test_given_dir_not_allowed(self):
        with (patch("src.commands.ls.access_error_message") as mock_error,
              patch("os.listdir") as mock_listdir,
              patch("src.commands.ls.print_data") as mock_print_data):
            mock_listdir.side_effect = PermissionError
            ls([], ["dir"])
            mock_listdir.assert_called_once_with(os.path.abspath("dir"))
            mock_print_data.assert_not_called()
            mock_error.assert_called_once_with("ls", "directory", "dir")

    def test_given_dir_not_exist(self):
        with (patch("src.commands.ls.not_exist_error_message") as mock_error,
              patch("os.listdir") as mock_listdir,
              patch("src.commands.ls.print_data") as mock_print_data):
            mock_listdir.side_effect = FileNotFoundError
            ls([], ["dir"])
            mock_listdir.assert_called_once_with(os.path.abspath("dir"))
            mock_print_data.assert_not_called()
            mock_error.assert_called_once_with("ls", "directory", "dir")

    def test_given_dir_not_a_directory(self):
        with (patch("src.commands.ls.wrong_type_error_message") as mock_error,
              patch("os.listdir") as mock_listdir,
              patch("src.commands.ls.print_data") as mock_print_data):
            mock_listdir.side_effect = NotADirectoryError
            ls([], ["dir"])
            mock_listdir.assert_called_once_with(os.path.abspath("dir"))
            mock_print_data.assert_not_called()
            mock_error.assert_called_once_with("ls", "directory", "dir")

    def test_given_dir_more_one_option(self):
        with (patch("src.commands.ls.invalid_arguments_error_message") as mock_error,
              patch("os.listdir") as mock_listdir,
              patch("src.commands.ls.print_data") as mock_print_data):
            ls(["-l", "-r"], ["dir"])
            mock_listdir.assert_not_called()
            mock_print_data.assert_not_called()
            mock_error.assert_called_once_with("ls")

    def test_given_dir_wrong_option(self):
        with (patch("src.commands.ls.invalid_option_error_message") as mock_error,
              patch("os.listdir") as mock_listdir,
              patch("src.commands.ls.print_data") as mock_print_data):
            ls(["-r"], ["dir"])
            mock_listdir.assert_not_called()
            mock_print_data.assert_not_called()
            mock_error.assert_called_once_with("ls", "-r")

    def test_given_dir_details(self):
        with (patch("logging.info") as mock_log,
              patch("os.listdir") as mock_listdir,
              patch("src.commands.ls.print_data") as mock_print_data):
            mock_listdir.return_value = ["file1", "file2"]
            ls(["-l"], ["dir"])
            mock_listdir.assert_called_once_with(os.path.abspath("dir"))
            mock_print_data.assert_called_once_with([
                os.path.join(os.path.abspath("dir"), "file1"),
                os.path.join(os.path.abspath("dir"), "file2")],
                details=True)
            mock_log.assert_called_once_with("Success")

    def test_given_dir_detais_not_allowed(self):
        with (patch("src.commands.ls.access_error_message") as mock_error,
              patch("os.listdir") as mock_listdir,
              patch("src.commands.ls.print_data") as mock_print_data):
            mock_listdir.side_effect = PermissionError
            ls(["-l"], ["dir"])
            mock_listdir.assert_called_once_with(os.path.abspath("dir"))
            mock_print_data.assert_not_called()
            mock_error.assert_called_once_with("ls", "directory", "dir")

    def test_given_dir_detais_not_exist(self):
        with (patch("src.commands.ls.not_exist_error_message") as mock_error,
              patch("os.listdir") as mock_listdir,
              patch("src.commands.ls.print_data") as mock_print_data):
            mock_listdir.side_effect = FileNotFoundError
            ls(["-l"], ["dir"])
            mock_listdir.assert_called_once_with(os.path.abspath("dir"))
            mock_print_data.assert_not_called()
            mock_error.assert_called_once_with("ls", "directory", "dir")
