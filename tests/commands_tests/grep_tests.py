import unittest
import os.path
from unittest.mock import patch
from src.commands.grep import grep


class GrepTestCase(unittest.TestCase):
    """Тесты для команы grep"""

    def test_dont_have_args(self):
        with (patch("src.commands.grep.invalid_arguments_error_message") as mock_error,
              patch("src.commands.grep.open") as mock_open,
              patch("src.commands.grep.print") as mock_print,
              patch("src.commands.grep.print_matches") as mock_print_matches):
            grep(["-i"], [])
            mock_open.assert_not_called()
            mock_print.assert_not_called()
            mock_print_matches.assert_not_called()
            mock_error.assert_called_once_with("grep")

    def test_one_arg(self):
        with (patch("src.commands.grep.invalid_arguments_error_message") as mock_error,
              patch("src.commands.grep.open") as mock_open,
              patch("src.commands.grep.print") as mock_print,
              patch("src.commands.grep.print_matches") as mock_print_matches):
            grep(["-i"], ["pattern"])
            mock_open.assert_not_called()
            mock_print.assert_not_called()
            mock_print_matches.assert_not_called()
            mock_error.assert_called_once_with("grep")

    def test_have_more_than_two_options(self):
        with (patch("src.commands.grep.invalid_arguments_error_message") as mock_error,
              patch("src.commands.grep.open") as mock_open,
              patch("src.commands.grep.print") as mock_print,
              patch("src.commands.grep.print_matches") as mock_print_matches):
            grep(["-r", "-i", "-l"], ["pattern", "file"])
            mock_open.assert_not_called()
            mock_print.assert_not_called()
            mock_print_matches.assert_not_called()
            mock_error.assert_called_once_with("grep")

    def test_have_more_than_two_args(self):
        with (patch("src.commands.grep.invalid_arguments_error_message") as mock_error,
              patch("src.commands.grep.open") as mock_open,
              patch("src.commands.grep.print") as mock_print,
              patch("src.commands.grep.print_matches") as mock_print_matches):
            grep(["-r", "-i"], ["pattern", "file", "arg"])
            mock_open.assert_not_called()
            mock_print.assert_not_called()
            mock_print_matches.assert_not_called()
            mock_error.assert_called_once_with("grep")

    def test_one_option_wrong(self):
        with (patch("src.commands.grep.invalid_option_error_message") as mock_error,
              patch("src.commands.grep.open") as mock_open,
              patch("src.commands.grep.print") as mock_print,
              patch("src.commands.grep.print_matches") as mock_print_matches):
            grep(["-l"], ["pattern", "file"])
            mock_open.assert_not_called()
            mock_print.assert_not_called()
            mock_print_matches.assert_not_called()
            mock_error.assert_called_once_with("grep", "-l")

    def test_two_option_first_wrong(self):
        with (patch("src.commands.grep.invalid_option_error_message") as mock_error,
              patch("src.commands.grep.open") as mock_open,
              patch("src.commands.grep.print") as mock_print,
              patch("src.commands.grep.print_matches") as mock_print_matches):
            grep(["-l", "-r"], ["pattern", "file"])
            mock_open.assert_not_called()
            mock_print.assert_not_called()
            mock_print_matches.assert_not_called()
            mock_error.assert_called_once_with("grep", "-l")

    def test_two_option_second_wrong(self):
        with (patch("src.commands.grep.invalid_option_error_message") as mock_error,
              patch("src.commands.grep.open") as mock_open,
              patch("src.commands.grep.print") as mock_print,
              patch("src.commands.grep.print_matches") as mock_print_matches):
            grep(["-r", "-l"], ["pattern", "file"])
            mock_open.assert_not_called()
            mock_print.assert_not_called()
            mock_print_matches.assert_not_called()
            mock_error.assert_called_once_with("grep", "-l")

    def test_not_exist(self):
        with (patch("src.commands.grep.not_exist_error_message") as mock_error,
              patch("src.commands.grep.open") as mock_open,
              patch("src.commands.grep.print_matches") as mock_print_matches,
              patch("src.commands.grep.print") as mock_print,
              patch("os.path.exists") as mock_exists):
            mock_exists.return_value = False
            grep([], ["pattern", "file"])
            mock_open.assert_not_called()
            mock_print.assert_not_called()
            mock_print_matches.assert_not_called()
            mock_error.assert_called_once_with("grep", "file or directory", "file")

    def test_file_with_recursive(self):
        with (patch("src.commands.grep.wrong_type_error_message") as mock_error,
              patch("src.commands.grep.open") as mock_open,
              patch("src.commands.grep.print") as mock_print,
              patch("src.commands.grep.print_matches") as mock_print_matches,
              patch("os.path.exists") as mock_exists,
              patch("os.path.isfile") as mock_isfile):
            mock_exists.return_value = True
            mock_isfile.return_value = True
            grep(["-i", "-r"], ["pattern", "file"])
            mock_open.assert_not_called()
            mock_print.assert_called_once_with("To work with a file don't use -r")
            mock_print_matches.assert_not_called()
            mock_error.assert_called_once_with("grep", "directory", "file")

    def test_file_correct_without_options(self):
        with (patch("logging.info") as mock_log,
              patch("src.commands.grep.open") as mock_open,
              patch("src.commands.grep.print") as mock_print,
              patch("src.commands.grep.print_matches") as mock_print_matches,
              patch("os.path.exists") as mock_exists,
              patch("os.path.isfile") as mock_isfile):
            mock_exists.return_value = True
            mock_isfile.return_value = True
            mock_print_matches.return_value = True
            grep([], ["pattern", "file"])
            mock_open.assert_called_once_with(os.path.abspath("file"),
                                              "r", encoding="utf-8")
            mock_print.assert_called()
            mock_print_matches.assert_called()
            mock_log.assert_called_once_with("Success")

    def test_file_correct_with_option(self):
        with (patch("logging.info") as mock_log,
              patch("src.commands.grep.open") as mock_open,
              patch("src.commands.grep.print") as mock_print,
              patch("src.commands.grep.print_matches") as mock_print_matches,
              patch("os.path.exists") as mock_exists,
              patch("os.path.isfile") as mock_isfile):
            mock_exists.return_value = True
            mock_isfile.return_value = True
            grep(["-i"], ["pattern", "file"])
            mock_open.assert_called_once_with(os.path.abspath("file"),
                                              "r", encoding="utf-8")
            mock_print.assert_called()
            mock_print_matches.assert_called()
            mock_log.assert_called_once_with("Success")

    def test_file_not_allowed(self):
        with (patch("src.commands.grep.access_error_message") as mock_error,
              patch("src.commands.grep.open") as mock_open,
              patch("src.commands.grep.print") as mock_print,
              patch("src.commands.grep.print_matches") as mock_print_matches,
              patch("os.path.exists") as mock_exists,
              patch("os.path.isfile") as mock_isfile):
            mock_exists.return_value = True
            mock_isfile.return_value = True
            mock_open.side_effect = PermissionError
            grep(["-i"], ["pattern", "file"])
            mock_open.assert_called_once_with(os.path.abspath("file"),
                                              "r", encoding="utf-8")
            mock_print.assert_not_called()
            mock_print_matches.assert_not_called()
            mock_error.assert_called_once_with("grep", "file", os.path.abspath("file"))

    def test_file_cant_decode(self):
        with (patch("src.commands.grep.decode_error_message") as mock_error,
              patch("src.commands.grep.open") as mock_open,
              patch("src.commands.grep.print") as mock_print,
              patch("src.commands.grep.print_matches") as mock_print_matches,
              patch("os.path.exists") as mock_exists,
              patch("os.path.isfile") as mock_isfile):
            mock_exists.return_value = True
            mock_isfile.return_value = True
            mock_open.side_effect = UnicodeDecodeError("utf-8", b"", 0, 0, "invalid start byte")
            grep(["-i"], ["pattern", "file"])
            mock_open.assert_called_once_with(os.path.abspath("file"),
                                              "r", encoding="utf-8")
            mock_print.assert_not_called()
            mock_print_matches.assert_not_called()
            mock_error.assert_called_once_with("grep", os.path.abspath("file"))

    def test_dir_without_recursive(self):
        with (patch("src.commands.grep.wrong_type_error_message") as mock_error,
              patch("src.commands.grep.open") as mock_open,
              patch("src.commands.grep.print") as mock_print,
              patch("src.commands.grep.print_matches") as mock_print_matches,
              patch("os.path.exists") as mock_exists,
              patch("os.path.isfile") as mock_isfile,
              patch("os.path.isdir") as mock_isdir):
            mock_exists.return_value = True
            mock_isfile.return_value = False
            mock_isdir.return_value = True
            grep(["-i"], ["pattern", "dir"])
            mock_open.assert_not_called()
            mock_print.assert_called_once_with("To work with a directory use -r")
            mock_print_matches.assert_not_called()
            mock_error.assert_called_once_with("grep", "file", "dir")

    def test_correct_dir(self):
        with (patch("logging.info") as mock_log,
              patch("src.commands.grep.open") as mock_open,
              patch("src.commands.grep.print") as _,
              patch("src.commands.grep.print_matches") as mock_print_matches,
              patch("os.walk") as mock_walk,
              patch("os.path.exists") as mock_exists,
              patch("os.path.isfile") as mock_isfile,
              patch("os.path.isdir") as mock_isdir):
            mock_exists.return_value = True
            mock_isfile.return_value = False
            mock_isdir.return_value = True
            mock_walk.return_value = [["dir1", "", ["file1", "file2"]]]
            grep(["-r"], ["pattern", "dir"])
            mock_walk.assert_called_once_with(os.path.abspath("dir"))
            mock_print_matches.assert_called()
            mock_open.assert_called()
            mock_log.assert_called_once_with("Success")

    def test_dir_not_allowed(self):
        with (patch("src.commands.grep.access_error_message") as mock_error,
              patch("src.commands.grep.open") as mock_open,
              patch("os.walk") as mock_walk,
              patch("src.commands.grep.print_matches") as mock_print_matches,
              patch("os.path.exists") as mock_exists,
              patch("os.path.isfile") as mock_isfile,
              patch("os.path.isdir") as mock_isdir):
            mock_exists.return_value = True
            mock_isfile.return_value = False
            mock_isdir.return_value = True
            mock_walk.side_effect = PermissionError
            grep(["-r"], ["pattern", "dir"])
            mock_walk.assert_called_once_with(os.path.abspath("dir"))
            mock_print_matches.assert_not_called()
            mock_open.assert_not_called()
            mock_error.assert_called_once_with("grep", "directory", "dir")
