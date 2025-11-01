import unittest
import os.path
from unittest.mock import patch, call
from src.commands.cat import cat


class CatTestCase(unittest.TestCase):
    """Тесты для команы cat"""

    def test_dont_have_paths(self):
        with (patch("src.commands.cat.invalid_arguments_error_message") as mock_error,
              patch("src.commands.cat.open") as mock_open):
            cat([], [])
            mock_open.assert_not_called()
            mock_error.assert_called_once_with("cat")

    def test_have_options(self):
        with (patch("src.commands.cat.invalid_arguments_error_message") as mock_error,
              patch("src.commands.cat.open") as mock_open):
            cat(["-r"], ["file_path"])
            mock_open.assert_not_called()
            mock_error.assert_called_once_with("cat")

    def test_have_more_than_one_path(self):
        with (patch("src.commands.cat.invalid_arguments_error_message") as mock_error,
              patch("src.commands.cat.open") as mock_open):
            cat([], ["file1_path", "file2_path"])
            mock_open.assert_not_called()
            mock_error.assert_called_once_with("cat")

    def test_correct_path(self):
        with (patch("src.commands.cat.open") as mock_open,
              patch("src.commands.cat.print") as mock_print,
              patch("logging.info") as mock_log,
              patch("os.path.exists") as mock_exists,
              patch("os.path.isfile") as mock_isfile):
            mock_exists.return_value = True
            mock_isfile.return_value = True
            cat([], ["file_path"])
            mock_open.assert_called_once_with(os.path.abspath("file_path"), "rb")
            mock_print.assert_called_once()
            mock_log.assert_called_once_with("Success")

    def test_not_exist(self):
        with (patch("src.commands.cat.open") as mock_open,
              patch("src.commands.cat.not_exist_error_message") as mock_error,
              patch("os.path.exists") as mock_exists):
            mock_exists.return_value = False
            cat([], ["file_path"])
            mock_open.assert_not_called()
            mock_error.assert_called_once_with("cat", "file", "file_path")

    def test_not_a_file(self):
        with (patch("src.commands.cat.open") as mock_open,
              patch("src.commands.cat.wrong_type_error_message") as mock_error,
              patch("os.path.exists") as mock_exists,
              patch("os.path.isfile") as mock_isfile):
            mock_exists.return_value = True
            mock_isfile.return_value = False
            cat([], ["file_path"])
            mock_open.assert_not_called()
            mock_error.assert_called_once_with("cat", "file", "file_path")

    def test_not_allowed(self):
        with (patch("src.commands.cat.open") as mock_open,
              patch("src.commands.cat.print") as mock_print,
              patch("src.commands.cat.access_error_message") as mock_error,
              patch("os.path.exists") as mock_exists,
              patch("os.path.isfile") as mock_isfile):
            mock_exists.return_value = True
            mock_isfile.return_value = True
            mock_open.side_effect = PermissionError
            cat([], ["file_path"])
            mock_open.assert_called_once_with(os.path.abspath("file_path"), "rb")
            mock_print.assert_not_called()
            mock_error.assert_called_once_with("cat", "file", "file_path")

    def test_cant_decode(self):
        with (patch("src.commands.cat.open") as mock_open,
              patch("src.commands.cat.print") as mock_print,
              patch("os.path.exists") as mock_exists,
              patch("os.path.isfile") as mock_isfile,
              patch("logging.info") as mock_log):
            mock_exists.return_value = True
            mock_isfile.return_value = True
            mock_file = mock_open.return_value.__enter__.return_value
            mock_open.side_effect = [UnicodeDecodeError("utf-8", b"", 0, 0, "invalid start byte"), mock_file]
            mock_open.side_effect
            cat([], ["file_path"])
            self.assertEqual(mock_open.call_args_list,
                             [call(os.path.abspath("file_path"), "rb"),
                              call(os.path.abspath("file_path"), "rb")])
            mock_print.assert_called_once()
            mock_log.assert_called_once_with("Success")
