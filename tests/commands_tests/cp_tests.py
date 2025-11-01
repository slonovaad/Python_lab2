import unittest
import os.path
from unittest.mock import patch
from src.commands.cp import cp
from src.constants.constants import HISTORY_FILE, UNDO_HISTORY_FILE, TRASH_DIRECTORY


class CpTestCase(unittest.TestCase):
    """Тесты для команы cp"""

    def test_less_than_two_paths(self):
        with (patch("src.commands.cp.invalid_arguments_error_message") as mock_error,
              patch("shutil.copy") as mock_copy,
              patch("shutil.copytree") as mock_copytree):
            cp([], ["file_path"])
            mock_copy.assert_not_called()
            mock_copytree.assert_not_called()
            mock_error.assert_called_once_with("cp")

    def test_have_more_than_one_options(self):
        with (patch("src.commands.cp.invalid_arguments_error_message") as mock_error,
              patch("shutil.copy") as mock_copy,
              patch("shutil.copytree") as mock_copytree):
            cp(["-r", "-l"], ["file_path1", "file_path2"])
            mock_copy.assert_not_called()
            mock_copytree.assert_not_called()
            mock_error.assert_called_once_with("cp")

    def test_more_than_two_paths(self):
        with (patch("src.commands.cp.invalid_arguments_error_message") as mock_error,
              patch("shutil.copy") as mock_copy,
              patch("shutil.copytree") as mock_copytree):
            cp([], ["file_path1", "file_path2", "file_path3"])
            mock_copy.assert_not_called()
            mock_copytree.assert_not_called()
            mock_error.assert_called_once_with("cp")

    def test_destination_is_history(self):
        with (patch("src.commands.cp.access_error_message") as mock_error,
              patch("shutil.copy") as mock_copy,
              patch("shutil.copytree") as mock_copytree):
            cp([], ["file_path1", HISTORY_FILE])
            mock_copy.assert_not_called()
            mock_copytree.assert_not_called()
            mock_error.assert_called_once_with("cp", "file or directory", HISTORY_FILE, action="change")

    def test_destination_is_undo_history(self):
        with (patch("src.commands.cp.access_error_message") as mock_error,
              patch("shutil.copy") as mock_copy,
              patch("shutil.copytree") as mock_copytree):
            cp([], ["file_path1", UNDO_HISTORY_FILE])
            mock_copy.assert_not_called()
            mock_copytree.assert_not_called()
            mock_error.assert_called_once_with("cp", "file or directory", UNDO_HISTORY_FILE, action="change")

    def test_destination_is_trash_dir(self):
        with (patch("src.commands.cp.access_error_message") as mock_error,
              patch("shutil.copy") as mock_copy,
              patch("shutil.copytree") as mock_copytree):
            cp([], ["path1", TRASH_DIRECTORY])
            mock_copy.assert_not_called()
            mock_copytree.assert_not_called()
            mock_error.assert_called_once_with("cp", "file or directory", TRASH_DIRECTORY, action="change")

    def test_destination_is_in_trash_dir(self):
        with (patch("src.commands.cp.access_error_message") as mock_error,
              patch("shutil.copy") as mock_copy,
              patch("shutil.copytree") as mock_copytree):
            cp([], ["path1", os.path.join(TRASH_DIRECTORY, "path2")])
            mock_copy.assert_not_called()
            mock_copytree.assert_not_called()
            mock_error.assert_called_once_with("cp", "file or directory", os.path.join(TRASH_DIRECTORY, "path2"),
                                               action="change")

    def test_destination_is_in_source(self):
        with (patch("src.commands.cp.in_parents_error_message") as mock_error,
              patch("shutil.copy") as mock_copy,
              patch("shutil.copytree") as mock_copytree):
            cp([], ["path1", os.path.join("path1", "path2")])
            mock_copy.assert_not_called()
            mock_copytree.assert_not_called()
            mock_error.assert_called_once_with("cp", "path1", os.path.join("path1", "path2"))

    def test_not_exist(self):
        with (patch("src.commands.cp.not_exist_error_message") as mock_error,
              patch("shutil.copy") as mock_copy,
              patch("shutil.copytree") as mock_copytree,
              patch("os.path.exists") as mock_exist):
            mock_exist.return_value = False
            cp([], ["path1", "path2"])
            mock_copy.assert_not_called()
            mock_copytree.assert_not_called()
            mock_error.assert_called_once_with("cp", "file or directory", "path1")

    def test_directory_without_option(self):
        with (patch("src.commands.cp.wrong_type_error_message") as mock_error,
              patch("src.commands.cp.print") as mock_print,
              patch("shutil.copy") as mock_copy,
              patch("shutil.copytree") as mock_copytree,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isfile") as mock_isfile):
            mock_exist.return_value = True
            mock_isfile.return_value = False
            cp([], ["path1", "path2"])
            mock_copy.assert_not_called()
            mock_copytree.assert_not_called()
            mock_error.assert_called_once_with("cp", "file", "path1")
            mock_print.assert_called_once_with("To copy a directory use -r")

    def test_correct_source_file_destination_directory(self):
        with (patch("src.commands.cp.write_to_history") as mock_undo_history,
              patch("src.commands.cp.make_reserve_copy") as mock_reserve_copy,
              patch("logging.info") as mock_log,
              patch("shutil.copy") as mock_copy,
              patch("shutil.copytree") as mock_copytree,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isfile") as mock_isfile,
              patch("os.makedirs") as mock_makedirs):
            mock_exist.return_value = True
            mock_isfile.return_value = True
            cp([], ["file", "directory/"])
            mock_makedirs.assert_called_once_with(os.path.abspath("directory/"), exist_ok=True)
            mock_copy.assert_called_once_with(os.path.abspath("file"),
                                              os.path.abspath(os.path.join("directory", "file")))
            mock_copytree.assert_not_called()
            mock_log.assert_called_once_with("Success")
            mock_reserve_copy.assert_called_once_with(os.path.abspath(os.path.join("directory", "file")))
            mock_undo_history.assert_called_once_with(UNDO_HISTORY_FILE,
                                                      f'cp "{os.path.abspath("file")}" "{
                                                      os.path.abspath(os.path.join("directory", "file"))}"')

    def test_source_file_destination_directory_not_allowed(self):
        with (patch("src.commands.cp.write_to_history") as mock_undo_history,
              patch("src.commands.cp.make_reserve_copy") as mock_reserve_copy,
              patch("src.commands.cp.access_error_message") as mock_error,
              patch("shutil.copy") as mock_copy,
              patch("shutil.copytree") as mock_copytree,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isfile") as mock_isfile,
              patch("os.makedirs") as mock_makedirs):
            mock_exist.return_value = True
            mock_isfile.return_value = True
            mock_copy.side_effect = PermissionError
            cp([], ["file", "directory/"])
            mock_makedirs.assert_called_once_with(os.path.abspath("directory/"), exist_ok=True)
            mock_copy.assert_called_once_with(os.path.abspath("file"),
                                              os.path.abspath(os.path.join("directory", "file")))
            mock_copytree.assert_not_called()
            mock_error.assert_called_once_with("cp", "file or directory", "file or directory/",
                                               action="read or change")
            mock_reserve_copy.assert_called_once_with(os.path.abspath(os.path.join("directory", "file")))
            mock_undo_history.assert_not_called()

    def test_correct_source_file_destination_file(self):
        with (patch("src.commands.cp.write_to_history") as mock_undo_history,
              patch("src.commands.cp.make_reserve_copy") as mock_reserve_copy,
              patch("logging.info") as mock_log,
              patch("shutil.copy") as mock_copy,
              patch("shutil.copytree") as mock_copytree,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isfile") as mock_isfile):
            mock_exist.return_value = True
            mock_isfile.return_value = True
            cp([], ["file1", "file2"])
            mock_copy.assert_called_once_with(os.path.abspath("file1"),
                                              os.path.abspath("file2"))
            mock_copytree.assert_not_called()
            mock_log.assert_called_once_with("Success")
            mock_reserve_copy.assert_called_once_with(os.path.abspath("file2"))
            mock_undo_history.assert_called_once_with(UNDO_HISTORY_FILE,
                                                      f'cp "{os.path.abspath("file1")}" "{
                                                      os.path.abspath("file2")}"')

    def test_source_file_destination_file_not_allowed(self):
        with (patch("src.commands.cp.write_to_history") as mock_undo_history,
              patch("src.commands.cp.make_reserve_copy") as mock_reserve_copy,
              patch("src.commands.cp.access_error_message") as mock_error,
              patch("shutil.copy") as mock_copy,
              patch("shutil.copytree") as mock_copytree,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isfile") as mock_isfile):
            mock_exist.return_value = True
            mock_isfile.return_value = True
            mock_copy.side_effect = PermissionError
            cp([], ["file1", "file2"])
            mock_copy.assert_called_once_with(os.path.abspath("file1"),
                                              os.path.abspath("file2"))
            mock_copytree.assert_not_called()
            mock_error.assert_called_once_with("cp", "file or directory", "file1 or file2",
                                               action="read or change")
            mock_reserve_copy.assert_called_once_with(os.path.abspath("file2"))
            mock_undo_history.assert_not_called()

    def test_wrong_option(self):
        with (patch("src.commands.cp.invalid_option_error_message") as mock_error,
              patch("shutil.copy") as mock_copy,
              patch("shutil.copytree") as mock_copytree,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isfile") as mock_isfile):
            mock_exist.return_value = True
            mock_isfile.return_value = True
            cp(["-l"], ["file1", "file2"])
            mock_copy.assert_not_called()
            mock_copytree.assert_not_called()
            mock_error.assert_called_once_with("cp", "-l")

    def test_file_with_option(self):
        with (patch("src.commands.cp.wrong_type_error_message") as mock_error,
              patch("src.commands.cp.print") as mock_print,
              patch("shutil.copy") as mock_copy,
              patch("shutil.copytree") as mock_copytree,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isfile") as mock_isfile):
            mock_exist.return_value = True
            mock_isfile.return_value = True
            cp(["-r"], ["path1", "path2"])
            mock_copy.assert_not_called()
            mock_copytree.assert_not_called()
            mock_error.assert_called_once_with("cp", "directory", "path1")
            mock_print.assert_called_once_with("To copy a file don't use -r")

    def test_correct_source_dir_destination_dir_with_slash(self):
        with (patch("logging.info") as mock_log,
              patch("src.commands.cp.make_reserve_copy") as mock_reserve_copy,
              patch("src.commands.cp.write_to_history") as mock_undo_history,
              patch("shutil.copy") as mock_copy,
              patch("shutil.copytree") as mock_copytree,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isdir") as mock_isdir,
              patch("os.makedirs") as mock_makedirs):
            mock_exist.return_value = True
            mock_isdir.return_value = True
            cp(["-r"], ["path1", "path2/"])
            mock_copy.assert_not_called()
            mock_reserve_copy.assert_called_once_with(os.path.abspath("path2/"))
            mock_makedirs.assert_called_once_with(os.path.abspath("path2/"), exist_ok=True)
            mock_copytree.assert_called_once_with(os.path.abspath("path1"),
                                                  os.path.abspath("path2/"), dirs_exist_ok=True)
            mock_log.assert_called_once_with("Success")
            mock_undo_history.assert_called_once_with(UNDO_HISTORY_FILE,
                                                      f'cp "{os.path.abspath("path1")}" "{
                                                      os.path.abspath("path2/")}"')

    def test_correct_source_dir_destination_dir_withot_slash(self):
        with (patch("logging.info") as mock_log,
              patch("src.commands.cp.make_reserve_copy") as mock_reserve_copy,
              patch("src.commands.cp.write_to_history") as mock_undo_history,
              patch("shutil.copy") as mock_copy,
              patch("shutil.copytree") as mock_copytree,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isdir") as mock_isdir,
              patch("os.makedirs") as mock_makedirs):
            mock_exist.return_value = True
            mock_isdir.return_value = True
            cp(["-r"], ["path1", "path2"])
            mock_copy.assert_not_called()
            mock_reserve_copy.assert_called_once_with(os.path.join(os.path.abspath("path2"), "path1"))
            mock_makedirs.assert_called_once_with(os.path.join(os.path.abspath("path2"), "path1"), exist_ok=True)
            mock_copytree.assert_called_once_with(os.path.abspath("path1"),
                                                  os.path.join(os.path.abspath("path2"), "path1"), dirs_exist_ok=True)
            mock_log.assert_called_once_with("Success")
            mock_undo_history.assert_called_once_with(UNDO_HISTORY_FILE,
                                                      f'cp "{os.path.abspath("path1")}" "{
                                                      os.path.join(os.path.abspath("path2"), "path1")}"')

    def test_source_dir_destination_dir_with_slash_not_allowed(self):
        with (patch("src.commands.cp.write_to_history") as mock_undo_history,
              patch("src.commands.cp.make_reserve_copy") as mock_reserve_copy,
              patch("src.commands.cp.access_error_message") as mock_error,
              patch("shutil.copy") as mock_copy,
              patch("shutil.copytree") as mock_copytree,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isdir") as mock_isdir,
              patch("os.makedirs") as mock_makedirs):
            mock_exist.return_value = True
            mock_isdir.return_value = True
            mock_copytree.side_effect = PermissionError
            cp(["-r"], ["path1", "path2/"])
            mock_copytree.assert_called_once_with(os.path.abspath("path1"),
                                                  os.path.abspath("path2/"), dirs_exist_ok=True)
            mock_makedirs.assert_called_once_with(os.path.abspath("path2/"), exist_ok=True)
            mock_copy.assert_not_called()
            mock_error.assert_called_once_with("cp", "directory", "path1 or path2/",
                                               action="read or change")
            mock_reserve_copy.assert_called_once_with(os.path.abspath("path2/"))
            mock_undo_history.assert_not_called()

    def test_source_dir_destination_dir_without_slash_not_allowed(self):
        with (patch("src.commands.cp.write_to_history") as mock_undo_history,
              patch("src.commands.cp.make_reserve_copy") as mock_reserve_copy,
              patch("src.commands.cp.access_error_message") as mock_error,
              patch("shutil.copy") as mock_copy,
              patch("shutil.copytree") as mock_copytree,
              patch("os.path.exists") as mock_exist,
              patch("os.path.isdir") as mock_isdir):
            mock_exist.return_value = True
            mock_isdir.return_value = True
            mock_copytree.side_effect = PermissionError
            cp(["-r"], ["path1", "path2"])
            mock_copytree.assert_called_once_with(os.path.abspath("path1"),
                                                  os.path.join(os.path.abspath("path2"), "path1"),
                                                  dirs_exist_ok=True)
            mock_copy.assert_not_called()
            mock_error.assert_called_once_with("cp", "directory", "path1 or path2",
                                               action="read or change")
            mock_reserve_copy.assert_called_once_with(os.path.join(os.path.abspath("path2"), "path1"))
            mock_undo_history.assert_not_called()
