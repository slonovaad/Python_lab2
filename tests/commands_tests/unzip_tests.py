import unittest
from unittest.mock import patch
import os.path
from src.commands.unzip import unzip


class UnzipTestCase(unittest.TestCase):
    """Тесты для команы unzip"""

    def test_dont_have_paths(self):
        with (patch("src.commands.unzip.invalid_arguments_error_message") as mock_error,
              patch("zipfile.ZipFile") as mock_unzip):
            unzip([], [])
            mock_unzip.assert_not_called()
            mock_error.assert_called_once_with("unzip")

    def test_have_more_than_onr_path(self):
        with (patch("src.commands.unzip.invalid_arguments_error_message") as mock_error,
              patch("zipfile.ZipFile") as mock_unzip):
            unzip([], ["path1", "path2"])
            mock_unzip.assert_not_called()
            mock_error.assert_called_once_with("unzip")

    def test_have_options(self):
        with (patch("src.commands.unzip.invalid_arguments_error_message") as mock_error,
              patch("zipfile.ZipFile") as mock_unzip):
            unzip(["-r"], ["path1"])
            mock_unzip.assert_not_called()
            mock_error.assert_called_once_with("unzip")

    def test_not_exist(self):
        with (patch("src.commands.unzip.not_exist_error_message") as mock_error,
              patch("zipfile.ZipFile") as mock_unzip,
              patch("os.path.exists") as mock_exist):
            mock_exist.return_value = False
            path = "path1"
            unzip([], [path])
            mock_unzip.assert_not_called()
            mock_error.assert_called_once_with("unzip", "file", path)

    def test_not_is_file(self):
        with (patch("src.commands.unzip.wrong_type_error_message") as mock_error,
              patch("zipfile.ZipFile") as mock_unzip,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isfile") as mock_isfile):
            mock_exist.return_value = True
            mock_isfile.return_value = False
            path = "path1"
            unzip([], [path])
            mock_unzip.assert_not_called()
            mock_error.assert_called_once_with("unzip", "file", path)

    def test_file_is_not_zip(self):
        with (patch("src.commands.unzip.wrong_type_error_message") as mock_error,
              patch("zipfile.ZipFile") as mock_unzip,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isfile") as mock_isfile):
            mock_exist.return_value = True
            mock_isfile.return_value = True
            path = "path1.mp3"
            unzip([], [path])
            mock_unzip.assert_not_called()
            mock_error.assert_called_once_with("unzip", "zip file", path)

    def test_correct(self):
        with (patch("logging.info") as mock_log,
              patch("zipfile.ZipFile") as mock_unzip,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isfile") as mock_isfile):
            mock_exist.return_value = True
            mock_isfile.return_value = True
            path = "path1.zip"
            unzip([], [path])
            mock_unzip.assert_called_once_with(os.path.abspath(path))
            mock_log.assert_called_once_with("Success")

    def test_not_allowed(self):
        with (patch("src.commands.unzip.access_error_message") as mock_error,
              patch("zipfile.ZipFile") as mock_unzip,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isfile") as mock_isfile):
            mock_exist.return_value = True
            mock_isfile.return_value = True
            mock_unzip.side_effect = PermissionError
            path = "path1.zip"
            unzip([], [path])
            mock_unzip.assert_called_once_with(os.path.abspath(path))
            mock_error.assert_called_once_with("unzip", "file", path)
