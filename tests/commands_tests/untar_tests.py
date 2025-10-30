import unittest
from unittest.mock import patch
import os.path
from src.commands.untar import untar


class UntarTestCase(unittest.TestCase):
    """Тесты для команы untar"""

    def test_dont_have_paths(self):
        with (patch("src.commands.untar.invalid_arguments_error_message") as mock_error,
              patch("tarfile.open") as mock_untar):
            untar([], [])
            mock_untar.assert_not_called()
            mock_error.assert_called_once_with("untar")

    def test_have_more_than_onr_path(self):
        with (patch("src.commands.untar.invalid_arguments_error_message") as mock_error,
              patch("tarfile.open") as mock_untar):
            untar([], ["path1", "path2"])
            mock_untar.assert_not_called()
            mock_error.assert_called_once_with("untar")

    def test_have_options(self):
        with (patch("src.commands.untar.invalid_arguments_error_message") as mock_error,
              patch("tarfile.open") as mock_untar):
            untar(["-r"], ["path1"])
            mock_untar.assert_not_called()
            mock_error.assert_called_once_with("untar")

    def test_not_exist(self):
        with (patch("src.commands.untar.not_exist_error_message") as mock_error,
              patch("tarfile.open") as mock_untar,
              patch("os.path.exists") as mock_exist):
            mock_exist.return_value = False
            path = "path1"
            untar([], [path])
            mock_untar.assert_not_called()
            mock_error.assert_called_once_with("untar", "file", path)

    def test_not_is_file(self):
        with (patch("src.commands.untar.wrong_type_error_message") as mock_error,
              patch("tarfile.open") as mock_untar,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isfile") as mock_isfile):
            mock_exist.return_value = True
            mock_isfile.return_value = False
            path = "path1"
            untar([], [path])
            mock_untar.assert_not_called()
            mock_error.assert_called_once_with("untar", "file", path)

    def test_file_is_not_tar(self):
        with (patch("src.commands.untar.wrong_type_error_message") as mock_error,
              patch("tarfile.open") as mock_untar,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isfile") as mock_isfile):
            mock_exist.return_value = True
            mock_isfile.return_value = True
            path = "path1.mp3"
            untar([], [path])
            mock_untar.assert_not_called()
            mock_error.assert_called_once_with("untar", "tar.gz file", path)

    def test_correct(self):
        with (patch("logging.info") as mock_log,
              patch("tarfile.open") as mock_untar,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isfile") as mock_isfile):
            mock_exist.return_value = True
            mock_isfile.return_value = True
            path = "path1.tar.gz"
            untar([], [path])
            mock_untar.assert_called_once_with(os.path.abspath(path))
            mock_log.assert_called_once_with("Success")

    def test_not_allowed(self):
        with (patch("src.commands.untar.access_error_message") as mock_error,
              patch("tarfile.open") as mock_untar,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isfile") as mock_isfile):
            mock_exist.return_value = True
            mock_isfile.return_value = True
            mock_untar.side_effect = PermissionError
            path = "path1.tar.gz"
            untar([], [path])
            mock_untar.assert_called_once_with(os.path.abspath(path))
            mock_error.assert_called_once_with("untar", "file", path)
