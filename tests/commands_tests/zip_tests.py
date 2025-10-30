import unittest
from unittest.mock import patch
import os.path
import zipfile
from src.commands.zip import zip


class ZipTestCase(unittest.TestCase):
    """Тесты для команы zip"""

    def test_dont_have_paths(self):
        with (patch("src.commands.zip.invalid_arguments_error_message") as mock_error,
              patch("zipfile.ZipFile") as mock_zip):
            zip([], [])
            mock_zip.assert_not_called()
            mock_error.assert_called_once_with("zip")

    def test_have_more_than_two_paths(self):
        with (patch("src.commands.zip.invalid_arguments_error_message") as mock_error,
              patch("zipfile.ZipFile") as mock_zip):
            zip([], ["path1", "path2", "path3"])
            mock_zip.assert_not_called()
            mock_error.assert_called_once_with("zip")

    def test_have_options(self):
        with (patch("src.commands.zip.invalid_arguments_error_message") as mock_error,
              patch("zipfile.ZipFile") as mock_zip):
            zip(["-r"], ["path1", "path2"])
            mock_zip.assert_not_called()
            mock_error.assert_called_once_with("zip")

    def test_not_exist(self):
        with (patch("src.commands.zip.not_exist_error_message") as mock_error,
              patch("zipfile.ZipFile") as mock_zip,
              patch("os.path.exists") as mock_exist):
            mock_exist.return_value = False
            source, destination = "path1", "path2.zip"
            zip([], [source, destination])
            mock_zip.assert_not_called()
            mock_error.assert_called_once_with("zip", "directory", source)

    def test_not_is_dir(self):
        with (patch("src.commands.zip.wrong_type_error_message") as mock_error,
              patch("zipfile.ZipFile") as mock_zip,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isdir") as mock_isdir):
            mock_exist.return_value = True
            mock_isdir.return_value = False
            source, destination = "path1", "path2.zip"
            zip([], [source, destination])
            mock_zip.assert_not_called()
            mock_error.assert_called_once_with("zip", "directory", source)

    def test_source_in_parents_of_destination(self):
        with (patch("src.commands.zip.in_parents_error_message") as mock_error,
              patch("zipfile.ZipFile") as mock_zip,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isdir") as mock_isdir):
            mock_exist.return_value = True
            mock_isdir.return_value = True
            source, destination = "path1", "path1/path2.zip"
            zip([], [source, destination])
            mock_zip.assert_not_called()
            mock_error.assert_called_once_with("zip", source, destination)

    def test_destination_is_not_zip(self):
        with (patch("src.commands.zip.wrong_type_error_message") as mock_error,
              patch("zipfile.ZipFile") as mock_zip,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isdir") as mock_isdir):
            mock_exist.return_value = True
            mock_isdir.return_value = True
            source, destination = "path1", "path2.mp3"
            zip([], [source, destination])
            mock_zip.assert_not_called()
            mock_error.assert_called_once_with("zip", "zip file", destination)

    def test_correct(self):
        with (patch("logging.info") as mock_log,
              patch("zipfile.ZipFile") as mock_zip,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isdir") as mock_isdir):
            mock_exist.return_value = True
            mock_isdir.return_value = True
            source, destination = "path1", "path2.zip"
            zip([], [source, destination])
            mock_zip.assert_called_once_with(os.path.abspath(destination), mode='w',
                                             compression=zipfile.ZIP_DEFLATED)
            mock_log.assert_called_once_with("Success")

    def test_correct_destination_is_dir(self):
        with (patch("logging.info") as mock_log,
              patch("zipfile.ZipFile") as mock_zip,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isdir") as mock_isdir,
              patch("os.makedirs") as mock_makedirs):
            mock_exist.return_value = True
            mock_isdir.return_value = True
            source, destination = "path1", "path2/"
            zip([], [source, destination])
            mock_makedirs.assert_called_once_with(os.path.abspath(destination), exist_ok=True)
            mock_zip.assert_called_once_with(
                os.path.join(os.path.abspath(destination),
                             os.path.basename(source) + ".zip"), mode='w',
                compression=zipfile.ZIP_DEFLATED)
            mock_log.assert_called_once_with("Success")

    def test_correct_one_path(self):
        with (patch("logging.info") as mock_log,
              patch("zipfile.ZipFile") as mock_zip,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isdir") as mock_isdir):
            mock_exist.return_value = True
            mock_isdir.return_value = True
            source = "path1"
            zip([], [source])
            mock_zip.assert_called_once_with(
                os.path.abspath(source) + ".zip", mode='w',
                compression=zipfile.ZIP_DEFLATED)
            mock_log.assert_called_once_with("Success")

    def test_not_allowed(self):
        with (patch("src.commands.zip.access_error_message") as mock_error,
              patch("zipfile.ZipFile") as mock_zip,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isdir") as mock_isdir):
            mock_exist.return_value = True
            mock_isdir.return_value = True
            mock_zip.side_effect = PermissionError
            source, destination = "path1", "path2.zip"
            zip([], [source, destination])
            mock_zip.assert_called_once_with(os.path.abspath(destination), mode='w',
                                             compression=zipfile.ZIP_DEFLATED)
            mock_error.assert_called_once_with("zip", "directory or file",
                                               f"{source} or {destination}", action="read or change")

    def test_not_allowed_one_path(self):
        with (patch("src.commands.zip.access_error_message") as mock_error,
              patch("zipfile.ZipFile") as mock_zip,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isdir") as mock_isdir):
            mock_exist.return_value = True
            mock_isdir.return_value = True
            mock_zip.side_effect = PermissionError
            source = "path1"
            zip([], [source])
            mock_zip.assert_called_once_with(
                os.path.abspath(source) + ".zip", mode='w',
                compression=zipfile.ZIP_DEFLATED)
            mock_error.assert_called_once_with("zip", "directory", source)

    def test_not_allowed_destination_is_dir(self):
        with (patch("src.commands.zip.access_error_message") as mock_error,
              patch("zipfile.ZipFile") as mock_zip,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isdir") as mock_isdir,
              patch("os.makedirs") as mock_makedirs):
            mock_exist.return_value = True
            mock_isdir.return_value = True
            mock_zip.side_effect = PermissionError
            source, destination = "path1", "path2/"
            zip([], [source, destination])
            mock_makedirs.assert_called_once_with(os.path.abspath(destination), exist_ok=True)
            mock_zip.assert_called_once_with(
                os.path.join(os.path.abspath(destination),
                             os.path.basename(source) + ".zip"), mode='w',
                compression=zipfile.ZIP_DEFLATED)
            mock_error.assert_called_once_with("zip", "directory or file",
                                               f"{source} or {destination}", action="read or change")
