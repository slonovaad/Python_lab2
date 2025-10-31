import unittest
from unittest.mock import patch, call
import os.path
from src.commands.mv import mv
from src.constants.constants import HISTORY_FILE, UNDO_HISTORY_FILE, TRASH_DIRECTORY


class MvTestCase(unittest.TestCase):
    """Тесты для команы mv"""

    def test_more_than_two_paths(self):
        with (patch("src.commands.mv.invalid_arguments_error_message") as mock_error,
              patch("os.rename") as mock_rename):
            mv([], ["path1", "path2", "path3"])
            mock_rename.assert_not_called()
            mock_error.assert_called_once_with("mv")

    def test_less_than_two_paths(self):
        with (patch("src.commands.mv.invalid_arguments_error_message") as mock_error,
              patch("os.rename") as mock_rename):
            mv([], ["path1"])
            mock_rename.assert_not_called()
            mock_error.assert_called_once_with("mv")

    def test_source_not_exist(self):
        with (patch("src.commands.mv.not_exist_error_message") as mock_error,
              patch("os.rename") as mock_rename,
              patch("os.path.exists") as mock_exists):
            mock_exists.return_value = False
            mv([], ["path1", "path2"])
            mock_rename.assert_not_called()
            mock_error.assert_called_once_with("mv", "file or directory", "path1")

    def test_source_is_history(self):
        with (patch("src.commands.mv.access_error_message") as mock_error,
              patch("os.rename") as mock_rename,
              patch("os.path.exists") as mock_exists):
            mock_exists.return_value = True
            mv([], [HISTORY_FILE, "path"])
            mock_rename.assert_not_called()
            mock_error.assert_called_once_with("mv", "file or directory",
                                               HISTORY_FILE, action="change")

    def test_source_is_undo_history(self):
        with (patch("src.commands.mv.access_error_message") as mock_error,
              patch("os.rename") as mock_rename,
              patch("os.path.exists") as mock_exists):
            mock_exists.return_value = True
            mv([], [UNDO_HISTORY_FILE, "path"])
            mock_rename.assert_not_called()
            mock_error.assert_called_once_with("mv", "file or directory",
                                               UNDO_HISTORY_FILE, action="change")

    def test_source_is_trash_dir(self):
        with (patch("src.commands.mv.access_error_message") as mock_error,
              patch("os.rename") as mock_rename,
              patch("os.path.exists") as mock_exists):
            mock_exists.return_value = True
            mv([], [TRASH_DIRECTORY, "path"])
            mock_rename.assert_not_called()
            mock_error.assert_called_once_with("mv", "file or directory",
                                               TRASH_DIRECTORY, action="change")

    def test_source_is_in_trash_dir(self):
        with (patch("src.commands.mv.access_error_message") as mock_error,
              patch("os.rename") as mock_rename,
              patch("os.path.exists") as mock_exists):
            mock_exists.return_value = True
            mv([],
               [os.path.join(TRASH_DIRECTORY, "path1"), "path2"])
            mock_rename.assert_not_called()
            mock_error.assert_called_once_with("mv", "file or directory",
                                               os.path.join(TRASH_DIRECTORY, "path1"),
                                               action="change")

    def test_source_is_current_dir(self):
        with (patch("src.commands.mv.is_current_dir_error_message") as mock_error,
              patch("os.rename") as mock_rename,
              patch("os.path.exists") as mock_exists):
            mock_exists.return_value = True
            mv([], [os.getcwd(), "path2"])
            mock_rename.assert_not_called()
            mock_error.assert_called_once_with("mv", os.getcwd(),
                                               action="move")

    def test_destination_is_current_dir(self):
        with (patch("src.commands.mv.is_current_dir_error_message") as mock_error,
              patch("os.rename") as mock_rename,
              patch("os.path.exists") as mock_exists):
            mock_exists.return_value = True
            mv([], ["path1", os.getcwd()])
            mock_rename.assert_not_called()
            mock_error.assert_called_once_with("mv", os.getcwd(),
                                               action="move")

    def test_source_is_not_allowed(self):
        with (patch("src.commands.mv.access_error_message") as mock_error,
              patch("os.rename") as mock_rename,
              patch("os.path.exists") as mock_exists,
              patch("os.access") as mock_access):
            mock_exists.return_value = True
            mock_access.return_value = False
            source, destination = "path1", "path2"
            mv([], [source, destination])
            mock_access.assert_called_once_with(os.path.abspath(source), os.W_OK)
            mock_rename.assert_not_called()
            mock_error.assert_called_once_with("mv", "file or directory",
                                               source, action="change")

    def test_destination_is_not_allowed(self):
        with (patch("src.commands.mv.access_error_message") as mock_error,
              patch("os.rename") as mock_rename,
              patch("os.path.exists") as mock_exists,
              patch("os.access") as mock_access):
            mock_exists.return_value = True
            mock_access.side_effect = [True, False]
            source, destination = "path1", "path2"
            mv([], [source, destination])
            mock_access.assert_called()
            self.assertEqual(mock_access.call_count, 2)
            self.assertEqual(mock_access.call_args_list,
                             [call(os.path.abspath(source), os.W_OK),
                              call(os.path.abspath(destination), os.W_OK)])
            mock_rename.assert_not_called()
            mock_error.assert_called_once_with("mv", "file or directory",
                                               destination, action="change")

    def test_destination_is_history(self):
        with (patch("src.commands.mv.access_error_message") as mock_error,
              patch("os.rename") as mock_rename,
              patch("os.path.exists") as mock_exists):
            mock_exists.return_value = True
            mv([], ["path", HISTORY_FILE])
            mock_rename.assert_not_called()
            mock_error.assert_called_once_with("mv", "file or directory",
                                               HISTORY_FILE, action="change")

    def test_destination_is_undo_history(self):
        with (patch("src.commands.mv.access_error_message") as mock_error,
              patch("os.rename") as mock_rename,
              patch("os.path.exists") as mock_exists):
            mock_exists.return_value = True
            mv([], ["path", UNDO_HISTORY_FILE])
            mock_rename.assert_not_called()
            mock_error.assert_called_once_with("mv", "file or directory",
                                               UNDO_HISTORY_FILE, action="change")

    def test_destination_is_trash_dir(self):
        with (patch("src.commands.mv.access_error_message") as mock_error,
              patch("os.rename") as mock_rename,
              patch("os.path.exists") as mock_exists):
            mock_exists.return_value = True
            mv([], ["path", TRASH_DIRECTORY])
            mock_rename.assert_not_called()
            mock_error.assert_called_once_with("mv", "file or directory",
                                               TRASH_DIRECTORY, action="change")

    def test_destination_is_in_trash_dir(self):
        with (patch("src.commands.mv.access_error_message") as mock_error,
              patch("os.rename") as mock_rename,
              patch("os.path.exists") as mock_exists):
            mock_exists.return_value = True
            mv([],
               ["path1", os.path.join(TRASH_DIRECTORY, "path2")])
            mock_rename.assert_not_called()
            mock_error.assert_called_once_with("mv", "file or directory",
                                               os.path.join(TRASH_DIRECTORY, "path2"),
                                               action="change")

    def test_source_in_parents_of_destination(self):
        with (patch("src.commands.mv.in_parents_error_message") as mock_error,
              patch("os.rename") as mock_rename,
              patch("os.path.exists") as mock_exists):
            mock_exists.return_value = True
            mv([],
               ["path1", "path1/path2"])
            mock_rename.assert_not_called()
            mock_error.assert_called_once_with("mv", "path1", "path1/path2")

    def test_destination_is_homedir(self):
        with (patch("src.commands.mv.access_error_message") as mock_error,
              patch("os.rename") as mock_rename,
              patch("os.path.exists") as mock_exists):
            mock_exists.return_value = True
            mv([],
               ["path", os.path.expanduser("~")])
            mock_rename.assert_not_called()
            mock_error.assert_called_once_with("mv", "directory",
                                               os.path.expanduser("~"), action="change")

    def test_source_is_homedir(self):
        with (patch("src.commands.mv.access_error_message") as mock_error,
              patch("os.rename") as mock_rename,
              patch("os.path.exists") as mock_exists):
            mock_exists.return_value = True
            mv([],
               [os.path.expanduser("~"), "/"])
            mock_rename.assert_not_called()
            mock_error.assert_called_once_with("mv", "directory",
                                               os.path.expanduser("~"), action="change")

    def test_correct_file(self):
        with (patch("logging.info") as mock_log,
              patch("os.rename") as mock_rename,
              patch("os.path.exists") as mock_exists,
              patch("os.path.isfile") as mock_isfile,
              patch("os.path.isdir") as mock_isdir,
              patch("os.makedirs") as mock_makedirs,
              patch("src.commands.mv.make_reserve_copy") as mock_reserve_copy,
              patch("src.commands.mv.write_to_history") as mock_history,
              patch("os.remove") as mock_remove,
              patch("shutil.rmtree") as mock_rmtree,
              patch("os.access") as mock_access):
            mock_exists.return_value = True
            mock_isfile.return_value = True
            mock_isdir.return_value = False
            mock_access.return_value = True
            mv([], ["path1", "path2/name"])
            mock_makedirs.assert_called_once_with(os.path.abspath("path2"), exist_ok=True)
            mock_reserve_copy.assert_called_once_with(os.path.abspath("path2/name"))
            mock_remove.assert_called_once_with(os.path.abspath("path2/name"))
            mock_rmtree.assert_not_called()
            mock_rename.assert_called_once_with(os.path.abspath("path1"),
                                                os.path.abspath("path2/name"))
            mock_log.assert_called_once_with("Success")
            mock_history.assert_called_once_with(UNDO_HISTORY_FILE,
                                                 f'mv "{os.path.abspath("path1")}" "{
                                                 os.path.abspath("path2/name")}"')

    def test_correct_file_destination_end_by_slash(self):
        with (patch("logging.info") as mock_log,
              patch("os.rename") as mock_rename,
              patch("os.path.exists") as mock_exists,
              patch("os.path.isfile") as mock_isfile,
              patch("os.path.isdir") as mock_isdir,
              patch("os.makedirs") as mock_makedirs,
              patch("src.commands.mv.make_reserve_copy") as mock_reserve_copy,
              patch("src.commands.mv.write_to_history") as mock_history,
              patch("os.remove") as mock_remove,
              patch("shutil.rmtree") as mock_rmtree,
              patch("os.access") as mock_access):
            mock_exists.return_value = True
            mock_isfile.return_value = True
            mock_isdir.return_value = False
            mock_access.return_value = True
            mv([], ["path1", "path2/name/"])
            mock_makedirs.assert_called_once_with(os.path.abspath("path2/name/"), exist_ok=True)
            mock_reserve_copy.assert_called_once_with(
                os.path.join(os.path.abspath("path2/name/"), "path1"))
            mock_remove.assert_called_once_with(
                os.path.join(os.path.abspath("path2/name/"), "path1"))
            mock_rmtree.assert_not_called()
            mock_rename.assert_called_once_with(os.path.abspath("path1"),
                                                os.path.join(os.path.abspath("path2/name/"), "path1"))
            mock_log.assert_called_once_with("Success")
            mock_history.assert_called_once_with(UNDO_HISTORY_FILE,
                                                 f'mv "{os.path.abspath("path1")}" "{
                                                 os.path.join(os.path.abspath("path2/name/"),
                                                              "path1")}"')

    def test_correct_dir(self):
        with (patch("logging.info") as mock_log,
              patch("os.rename") as mock_rename,
              patch("os.path.exists") as mock_exists,
              patch("os.path.isfile") as mock_isfile,
              patch("os.path.isdir") as mock_isdir,
              patch("os.makedirs") as mock_makedirs,
              patch("src.commands.mv.make_reserve_copy") as mock_reserve_copy,
              patch("src.commands.mv.write_to_history") as mock_history,
              patch("os.remove") as mock_remove,
              patch("shutil.rmtree") as mock_rmtree,
              patch("os.access") as mock_access):
            mock_exists.return_value = True
            mock_isfile.return_value = False
            mock_isdir.return_value = True
            mock_access.return_value = True
            source, destination = "path1", "path2/name"
            mv([], [source, destination])
            mock_makedirs.assert_called_once_with(os.path.abspath("path2"), exist_ok=True)
            mock_reserve_copy.assert_called_once_with(os.path.abspath(destination))
            mock_remove.assert_not_called()
            mock_rmtree.assert_called_once_with(os.path.abspath(destination))
            mock_rename.assert_called_once_with(os.path.abspath(source),
                                                os.path.abspath(destination))
            mock_log.assert_called_once_with("Success")
            mock_history.assert_called_once_with(UNDO_HISTORY_FILE,
                                                 f'mv "{os.path.abspath(source)}" "{
                                                 os.path.abspath(destination)}"')

    def test_correct_dir_destination_end_by_slash(self):
        with (patch("logging.info") as mock_log,
              patch("os.rename") as mock_rename,
              patch("os.path.exists") as mock_exists,
              patch("os.path.isfile") as mock_isfile,
              patch("os.path.isdir") as mock_isdir,
              patch("os.makedirs") as mock_makedirs,
              patch("src.commands.mv.make_reserve_copy") as mock_reserve_copy,
              patch("src.commands.mv.write_to_history") as mock_history,
              patch("os.remove") as mock_remove,
              patch("shutil.rmtree") as mock_rmtree,
              patch("os.access") as mock_access):
            mock_exists.return_value = True
            mock_isfile.return_value = False
            mock_isdir.return_value = True
            mock_access.return_value = True
            source, destination = "path1", "path2/name/"
            mv([], [source, destination])
            mock_makedirs.assert_called_once_with(os.path.abspath(destination), exist_ok=True)
            mock_reserve_copy.assert_called_once_with(
                os.path.join(os.path.abspath(destination), source))
            mock_remove.assert_not_called()
            mock_rmtree.assert_called_once_with(
                os.path.join(os.path.abspath(destination), source))
            mock_rename.assert_called_once_with(os.path.abspath(source),
                                                os.path.join(os.path.abspath(destination), source))
            mock_log.assert_called_once_with("Success")
            mock_history.assert_called_once_with(UNDO_HISTORY_FILE,
                                                 f'mv "{os.path.abspath(source)}" "{
                                                 os.path.join(os.path.abspath(destination),
                                                              source)}"')
