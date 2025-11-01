import unittest
import os
from unittest.mock import patch
from src.make_reserve_copy import make_reserve_copy
from src.constants.constants import TRASH_DIRECTORY


class MakeReserveCopyTestCase(unittest.TestCase):
    """Тесты для функции make_reserve_copy"""

    def test_file_when_trash_dir_exists(self):
        with (patch("src.make_reserve_copy.get_command_number") as mock_get_number,
              patch("os.path.exists") as mock_exists,
              patch("os.path.isfile") as mock_isfile,
              patch("os.path.isdir") as mock_isdir,
              patch("os.makedirs") as mock_makedirs,
              patch("shutil.copy") as mock_copy,
              patch("shutil.copytree") as mock_copytree):
            mock_exists.return_value = True
            mock_isfile.return_value = True
            mock_isdir.return_value = False
            mock_get_number.return_value = 2
            path = "path1"
            make_reserve_copy(path)
            mock_get_number.assert_called_once()
            mock_makedirs.assert_not_called()
            mock_copy.assert_called_once_with(path, os.path.join(TRASH_DIRECTORY, f"2_{path}"))
            mock_copytree.assert_not_called()

    def test_file_when_trash_dir_not_exists(self):
        with (patch("src.make_reserve_copy.get_command_number") as mock_get_number,
              patch("os.path.exists") as mock_exists,
              patch("os.path.isfile") as mock_isfile,
              patch("os.path.isdir") as mock_isdir,
              patch("os.makedirs") as mock_makedirs,
              patch("shutil.copy") as mock_copy,
              patch("shutil.copytree") as mock_copytree):
            mock_exists.return_value = False
            mock_isfile.return_value = True
            mock_isdir.return_value = False
            mock_get_number.return_value = 1
            path = "path1"
            make_reserve_copy(path)
            mock_get_number.assert_called_once()
            mock_makedirs.assert_called_once_with(TRASH_DIRECTORY)
            mock_copy.assert_called_once_with(path, os.path.join(TRASH_DIRECTORY, f"1_{path}"))
            mock_copytree.assert_not_called()

    def test_dir_when_trash_dir_exists(self):
        with (patch("src.make_reserve_copy.get_command_number") as mock_get_number,
              patch("os.path.exists") as mock_exists,
              patch("os.path.isfile") as mock_isfile,
              patch("os.path.isdir") as mock_isdir,
              patch("os.makedirs") as mock_makedirs,
              patch("shutil.copy") as mock_copy,
              patch("shutil.copytree") as mock_copytree):
            mock_exists.return_value = True
            mock_isfile.return_value = False
            mock_isdir.return_value = True
            mock_get_number.return_value = 2
            path = "path1"
            make_reserve_copy(path)
            mock_get_number.assert_called_once()
            mock_makedirs.assert_not_called()
            mock_copytree.assert_called_once_with(path, os.path.join(TRASH_DIRECTORY, f"2_{path}"))
            mock_copy.assert_not_called()

    def test_dir_when_trash_dir_not_exists(self):
        with (patch("src.make_reserve_copy.get_command_number") as mock_get_number,
              patch("os.path.exists") as mock_exists,
              patch("os.path.isfile") as mock_isfile,
              patch("os.path.isdir") as mock_isdir,
              patch("os.makedirs") as mock_makedirs,
              patch("shutil.copy") as mock_copy,
              patch("shutil.copytree") as mock_copytree):
            mock_exists.return_value = False
            mock_isfile.return_value = False
            mock_isdir.return_value = True
            path = "path1"
            mock_get_number.return_value = 1
            make_reserve_copy(path)
            mock_get_number.assert_called_once()
            mock_makedirs.assert_called_once_with(TRASH_DIRECTORY)
            mock_copytree.assert_called_once_with(path, os.path.join(TRASH_DIRECTORY, f"1_{path}"))
            mock_copy.assert_not_called()
