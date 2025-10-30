import unittest
from unittest.mock import patch
import os.path
from src.commands.rm import rm
from src.constants.constants import HISTORY_FILE, UNDO_HISTORY_FILE, TRASH_DIRECTORY


class RmTestCase(unittest.TestCase):
    """Тесты для команы rm"""

    def test_dont_have_paths(self):
        with (patch("src.commands.rm.invalid_arguments_error_message") as mock_error,
              patch("os.remove") as mock_remove,
              patch("shutil.rmtree") as mock_rmtree):
            rm([], [])
            mock_remove.assert_not_called()
            mock_rmtree.assert_not_called()
            mock_error.assert_called_once_with("rm")

    def test_more_than_one_paths(self):
        with (patch("src.commands.rm.invalid_arguments_error_message") as mock_error,
              patch("os.remove") as mock_remove,
              patch("shutil.rmtree") as mock_rmtree):
            rm([], ["path1", "path2"])
            mock_remove.assert_not_called()
            mock_rmtree.assert_not_called()
            mock_error.assert_called_once_with("rm")

    def test_more_than_one_option(self):
        with (patch("src.commands.rm.invalid_arguments_error_message") as mock_error,
              patch("os.remove") as mock_remove,
              patch("shutil.rmtree") as mock_rmtree):
            rm(["-r", "-l"], ["path1"])
            mock_remove.assert_not_called()
            mock_rmtree.assert_not_called()
            mock_error.assert_called_once_with("rm")

    def test_not_exist(self):
        with (patch("src.commands.rm.not_exist_error_message") as mock_error,
              patch("os.remove") as mock_remove,
              patch("shutil.rmtree") as mock_rmtree,
              patch("os.path.exists") as mock_exists):
            mock_exists.return_value = False
            path = "path1"
            rm([], [path])
            mock_remove.assert_not_called()
            mock_rmtree.assert_not_called()
            mock_error.assert_called_once_with("rm", "file or directory", path)

    def test_is_parent(self):
        with (patch("src.commands.rm.in_parents_error_message") as mock_error,
              patch("os.remove") as mock_remove,
              patch("shutil.rmtree") as mock_rmtree,
              patch("os.path.exists") as mock_exists):
            mock_exists.return_value = True
            path = os.path.dirname(os.getcwd())
            rm([], [path])
            mock_remove.assert_not_called()
            mock_rmtree.assert_not_called()
            mock_error.assert_called_once_with("rm", path, "current directory")

    def test_is_current_dir(self):
        with (patch("src.commands.rm.is_current_dir_error_message") as mock_error,
              patch("os.remove") as mock_remove,
              patch("shutil.rmtree") as mock_rmtree,
              patch("os.path.exists") as mock_exists):
            mock_exists.return_value = True
            path = os.getcwd()
            rm([], [path])
            mock_remove.assert_not_called()
            mock_rmtree.assert_not_called()
            mock_error.assert_called_once_with("rm", path, "remove")

    def test_is_history(self):
        with (patch("src.commands.rm.access_error_message") as mock_error,
              patch("os.remove") as mock_remove,
              patch("shutil.rmtree") as mock_rmtree,
              patch("os.path.exists") as mock_exists):
            mock_exists.return_value = True
            path = HISTORY_FILE
            rm([], [path])
            mock_remove.assert_not_called()
            mock_rmtree.assert_not_called()
            mock_error.assert_called_once_with("rm", "file or directory",
                                               path, action="remove")

    def test_is_undo_history(self):
        with (patch("src.commands.rm.access_error_message") as mock_error,
              patch("os.remove") as mock_remove,
              patch("shutil.rmtree") as mock_rmtree,
              patch("os.path.exists") as mock_exists):
            mock_exists.return_value = True
            path = UNDO_HISTORY_FILE
            rm([], [path])
            mock_remove.assert_not_called()
            mock_rmtree.assert_not_called()
            mock_error.assert_called_once_with("rm", "file or directory",
                                               path, action="remove")

    def test_is_trash_dir(self):
        with (patch("src.commands.rm.access_error_message") as mock_error,
              patch("os.remove") as mock_remove,
              patch("shutil.rmtree") as mock_rmtree,
              patch("os.path.exists") as mock_exists):
            mock_exists.return_value = True
            path = TRASH_DIRECTORY
            rm([], [path])
            mock_remove.assert_not_called()
            mock_rmtree.assert_not_called()
            mock_error.assert_called_once_with("rm", "file or directory",
                                               path, action="remove")

    def test_is_in_trash_dir(self):
        with (patch("src.commands.rm.access_error_message") as mock_error,
              patch("os.remove") as mock_remove,
              patch("shutil.rmtree") as mock_rmtree,
              patch("os.path.exists") as mock_exists):
            mock_exists.return_value = True
            path = os.path.join(TRASH_DIRECTORY, "path")
            rm([], [path])
            mock_remove.assert_not_called()
            mock_rmtree.assert_not_called()
            mock_error.assert_called_once_with("rm", "file or directory",
                                               path, action="remove")

    def test_dir_without_recursive(self):
        with (patch("src.commands.rm.wrong_type_error_message") as mock_error,
              patch("os.remove") as mock_remove,
              patch("shutil.rmtree") as mock_rmtree,
              patch("os.path.exists") as mock_exists,
              patch("os.path.isfile") as mock_isfile,
              patch("src.commands.rm.print") as mock_print):
            mock_exists.return_value = True
            mock_isfile.return_value = False
            path = "path"
            rm([], [path])
            mock_remove.assert_not_called()
            mock_rmtree.assert_not_called()
            mock_error.assert_called_once_with("rm", "file", path)
            mock_print.assert_called_once_with("To remove a directory use -r")

    def test_file_correct(self):
        with (patch("logging.info") as mock_log,
              patch("os.remove") as mock_remove,
              patch("shutil.rmtree") as mock_rmtree,
              patch("os.path.exists") as mock_exists,
              patch("os.path.isfile") as mock_isfile,
              patch("src.commands.rm.make_reserve_copy") as mock_reserve_copy,
              patch("src.commands.rm.write_to_history") as mock_history):
            mock_exists.return_value = True
            mock_isfile.return_value = True
            path = "path"
            rm([], [path])
            mock_remove.assert_called_once_with(os.path.abspath(path))
            mock_rmtree.assert_not_called()
            mock_reserve_copy.assert_called_once_with(os.path.abspath(path))
            mock_history.assert_called_once_with(UNDO_HISTORY_FILE,
                                                 f'rm "{os.path.abspath(path)}"')
            mock_log.assert_called_once_with("Success")

    def test_file_not_allowed(self):
        with (patch("src.commands.rm.access_error_message") as mock_error,
              patch("os.remove") as mock_remove,
              patch("shutil.rmtree") as mock_rmtree,
              patch("os.path.exists") as mock_exists,
              patch("os.path.isfile") as mock_isfile,
              patch("src.commands.rm.make_reserve_copy") as mock_reserve_copy,
              patch("src.commands.rm.write_to_history") as mock_history):
            mock_exists.return_value = True
            mock_isfile.return_value = True
            mock_remove.side_effect = PermissionError
            path = "path"
            rm([], [path])
            mock_remove.assert_called_once_with(os.path.abspath(path))
            mock_rmtree.assert_not_called()
            mock_reserve_copy.assert_called_once_with(os.path.abspath(path))
            mock_history.assert_not_called()
            mock_error.assert_called_once_with("rm", "file", path, action="remove")

    def test_wrong_option(self):
        with (patch("src.commands.rm.invalid_option_error_message") as mock_error,
              patch("os.remove") as mock_remove,
              patch("shutil.rmtree") as mock_rmtree,
              patch("os.path.exists") as mock_exists):
            mock_exists.return_value = True
            path = "path"
            rm(["-l"], [path])
            mock_remove.assert_not_called()
            mock_rmtree.assert_not_called()
            mock_error.assert_called_once_with("rm", "-l")

    def test_file_with_recursive(self):
        with (patch("src.commands.rm.wrong_type_error_message") as mock_error,
              patch("os.remove") as mock_remove,
              patch("shutil.rmtree") as mock_rmtree,
              patch("os.path.exists") as mock_exists,
              patch("os.path.isdir") as mock_isdir,
              patch("src.commands.rm.print") as mock_print):
            mock_exists.return_value = True
            mock_isdir.return_value = False
            path = "path"
            rm(["-r"], [path])
            mock_remove.assert_not_called()
            mock_rmtree.assert_not_called()
            mock_error.assert_called_once_with("rm", "directory", path)
            mock_print.assert_called_once_with("To remove a file don't use -r")

    def test_dir_correct(self):
        with (patch("logging.info") as mock_log,
              patch("os.remove") as mock_remove,
              patch("shutil.rmtree") as mock_rmtree,
              patch("os.path.exists") as mock_exists,
              patch("os.path.isdir") as mock_isdir,
              patch("src.commands.rm.input") as mock_input,
              patch("src.commands.rm.make_reserve_copy") as mock_reserve_copy,
              patch("src.commands.rm.write_to_history") as mock_history):
            mock_exists.return_value = True
            mock_isdir.return_value = True
            mock_input.return_value = "y"
            path = "path"
            rm(["-r"], [path])
            mock_remove.assert_not_called()
            mock_input.assert_called_once_with("Are you sure you want to remove this directory? [y/n] ")
            mock_rmtree.assert_called_once_with(os.path.abspath(path))
            mock_reserve_copy.assert_called_once_with(os.path.abspath(path))
            mock_history.assert_called_once_with(UNDO_HISTORY_FILE,
                                                 f'rm "{os.path.abspath(path)}"')
            mock_log.assert_called_once_with("Success")

    def test_dir_permission_error(self):
        with (patch("src.commands.rm.access_error_message") as mock_error,
              patch("os.remove") as mock_remove,
              patch("shutil.rmtree") as mock_rmtree,
              patch("os.path.exists") as mock_exists,
              patch("os.path.isdir") as mock_isdir,
              patch("src.commands.rm.input") as mock_input,
              patch("src.commands.rm.make_reserve_copy") as mock_reserve_copy,
              patch("src.commands.rm.write_to_history") as mock_history):
            mock_exists.return_value = True
            mock_isdir.return_value = True
            mock_input.return_value = "y"
            mock_rmtree.side_effect = PermissionError
            path = "path"
            rm(["-r"], [path])
            mock_remove.assert_not_called()
            mock_input.assert_called_once_with("Are you sure you want to remove this directory? [y/n] ")
            mock_rmtree.assert_called_once_with(os.path.abspath(path))
            mock_reserve_copy.assert_called_once_with(os.path.abspath(path))
            mock_history.assert_not_called()
            mock_error.assert_called_once_with("rm", "directory", path, action="remove")

    def test_dir_didnt_confimated(self):
        with (patch("logging.info") as mock_log,
              patch("os.remove") as mock_remove,
              patch("shutil.rmtree") as mock_rmtree,
              patch("os.path.exists") as mock_exists,
              patch("os.path.isdir") as mock_isdir,
              patch("src.commands.rm.input") as mock_input,
              patch("src.commands.rm.make_reserve_copy") as mock_reserve_copy,
              patch("src.commands.rm.write_to_history") as mock_history):
            mock_exists.return_value = True
            mock_isdir.return_value = True
            mock_input.return_value = "n"
            path = "path"
            rm(["-r"], [path])
            mock_remove.assert_not_called()
            mock_input.assert_called_once_with("Are you sure you want to remove this directory? [y/n] ")
            mock_rmtree.assert_not_called()
            mock_reserve_copy.assert_not_called()
            mock_history.assert_not_called()
            mock_log.assert_called_once_with("Didn't confirmated")
