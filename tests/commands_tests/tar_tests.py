import unittest
from unittest.mock import patch
import os.path
from src.commands.tar import tar


class TarTestCase(unittest.TestCase):
    """Тесты для команы tar"""

    def test_dont_have_paths(self):
        with (patch("src.commands.tar.invalid_arguments_error_message") as mock_error,
              patch("tarfile.open") as mock_tar):
            tar([], [])
            mock_tar.assert_not_called()
            mock_error.assert_called_once_with("tar")

    def test_have_more_than_two_paths(self):
        with (patch("src.commands.tar.invalid_arguments_error_message") as mock_error,
              patch("tarfile.open") as mock_tar):
            tar([], ["path1", "path2", "path3"])
            mock_tar.assert_not_called()
            mock_error.assert_called_once_with("tar")

    def test_have_options(self):
        with (patch("src.commands.tar.invalid_arguments_error_message") as mock_error,
              patch("tarfile.open") as mock_tar):
            tar(["-r"], ["path1", "path2"])
            mock_tar.assert_not_called()
            mock_error.assert_called_once_with("tar")

    def test_not_exist(self):
        with (patch("src.commands.tar.not_exist_error_message") as mock_error,
              patch("tarfile.open") as mock_tar,
              patch("os.path.exists") as mock_exist):
            mock_exist.return_value = False
            source, destination = "path1", "path2.tar.gz"
            tar([], [source, destination])
            mock_tar.assert_not_called()
            mock_error.assert_called_once_with("tar", "directory", source)

    def test_not_is_dir(self):
        with (patch("src.commands.tar.wrong_type_error_message") as mock_error,
              patch("tarfile.open") as mock_tar,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isdir") as mock_isdir):
            mock_exist.return_value = True
            mock_isdir.return_value = False
            source, destination = "path1", "path2.tar.gz"
            tar([], [source, destination])
            mock_tar.assert_not_called()
            mock_error.assert_called_once_with("tar", "directory", source)

    def test_source_in_parents_of_destination(self):
        with (patch("src.commands.tar.in_parents_error_message") as mock_error,
              patch("tarfile.open") as mock_tar,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isdir") as mock_isdir):
            mock_exist.return_value = True
            mock_isdir.return_value = True
            source, destination = "path1", "path1/path2.tar.gz"
            tar([], [source, destination])
            mock_tar.assert_not_called()
            mock_error.assert_called_once_with("tar", source, destination)

    def test_destination_is_not_tar(self):
        with (patch("src.commands.tar.wrong_type_error_message") as mock_error,
              patch("tarfile.open") as mock_tar,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isdir") as mock_isdir):
            mock_exist.return_value = True
            mock_isdir.return_value = True
            source, destination = "path1", "path2.mp3"
            tar([], [source, destination])
            mock_tar.assert_not_called()
            mock_error.assert_called_once_with("tar", "tar.gz file", destination)

    def test_correct(self):
        with (patch("logging.info") as mock_log,
              patch("tarfile.open") as mock_tar,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isdir") as mock_isdir):
            mock_exist.return_value = True
            mock_isdir.return_value = True
            source, destination = "path1", "path2.tar.gz"
            tar([], [source, destination])
            mock_tar.assert_called_once_with(os.path.abspath(destination), "w:gz")
            mock_log.assert_called_once_with("Success")

    def test_correct_destination_is_dir(self):
        with (patch("logging.info") as mock_log,
              patch("tarfile.open") as mock_tar,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isdir") as mock_isdir,
              patch("os.makedirs") as mock_makedirs):
            mock_exist.return_value = True
            mock_isdir.return_value = True
            source, destination = "path1", "path2/"
            tar([], [source, destination])
            mock_makedirs.assert_called_once_with(os.path.abspath(destination), exist_ok=True)
            mock_tar.assert_called_once_with(
                os.path.join(os.path.abspath(destination),
                             os.path.basename(source) + ".tar.gz"), "w:gz")
            mock_log.assert_called_once_with("Success")

    def test_correct_one_path(self):
        with (patch("logging.info") as mock_log,
              patch("tarfile.open") as mock_tar,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isdir") as mock_isdir):
            mock_exist.return_value = True
            mock_isdir.return_value = True
            source = "path1"
            tar([], [source])
            mock_tar.assert_called_once_with(
                os.path.abspath(source) + ".tar.gz", "w:gz")
            mock_log.assert_called_once_with("Success")

    def test_not_allowed(self):
        with (patch("src.commands.tar.access_error_message") as mock_error,
              patch("tarfile.open") as mock_tar,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isdir") as mock_isdir):
            mock_exist.return_value = True
            mock_isdir.return_value = True
            mock_tar.side_effect = PermissionError
            source, destination = "path1", "path2.tar.gz"
            tar([], [source, destination])
            mock_tar.assert_called_once_with(os.path.abspath(destination), "w:gz")
            mock_error.assert_called_once_with("tar", "directory or file",
                                               f"{source} or {destination}", action="read or change")

    def test_not_allowed_one_path(self):
        with (patch("src.commands.tar.access_error_message") as mock_error,
              patch("tarfile.open") as mock_tar,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isdir") as mock_isdir):
            mock_exist.return_value = True
            mock_isdir.return_value = True
            mock_tar.side_effect = PermissionError
            source = "path1"
            tar([], [source])
            mock_tar.assert_called_once_with(
                os.path.abspath(source) + ".tar.gz", "w:gz")
            mock_error.assert_called_once_with("tar", "directory", source)

    def test_not_allowed_destination_is_dir(self):
        with (patch("src.commands.tar.access_error_message") as mock_error,
              patch("tarfile.open") as mock_tar,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isdir") as mock_isdir,
              patch("os.makedirs") as mock_makedirs):
            mock_exist.return_value = True
            mock_isdir.return_value = True
            mock_tar.side_effect = PermissionError
            source, destination = "path1", "path2/"
            tar([], [source, destination])
            mock_makedirs.assert_called_once_with(os.path.abspath(destination), exist_ok=True)
            mock_tar.assert_called_once_with(
                os.path.join(os.path.abspath(destination),
                             os.path.basename(source) + ".tar.gz"), "w:gz")
            mock_error.assert_called_once_with("tar", "directory or file",
                                               f"{source} or {destination}", action="read or change")
