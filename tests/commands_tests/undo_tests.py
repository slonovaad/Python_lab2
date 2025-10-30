import os.path
import unittest
from unittest.mock import patch, call
from src.commands.undo import undo
from src.constants.constants import UNDO_HISTORY_FILE, TRASH_DIRECTORY


class UndoTestCase(unittest.TestCase):
    """Тесты для команы undo"""

    def test_have_arguments(self):
        with (patch("logging.info") as mock_log,
              patch("src.commands.undo.invalid_arguments_error_message") as mock_error):
            undo([], ["path"])
            mock_error.assert_called_once_with("undo")
            mock_log.assert_not_called()

    def test_have_options(self):
        with (patch("logging.info") as mock_log,
              patch("src.commands.undo.invalid_arguments_error_message") as mock_error):
            undo(["-r"], [])
            mock_error.assert_called_once_with("undo")
            mock_log.assert_not_called()

    def test_no_commands_in_history_file_not_exist(self):
        with (patch("logging.info") as mock_log,
              patch("src.commands.undo.not_exist_error_message") as mock_error,
              patch("os.path.exists") as mock_exists):
            mock_exists.return_value = False
            undo([], [])
            mock_error.assert_called_once_with("undo", "commands in history", "cp, mv, rm")
            mock_log.assert_not_called()

    def test_no_commands_in_history_file_exist(self):
        with (patch("logging.info") as mock_log,
              patch("src.commands.undo.not_exist_error_message") as mock_error,
              patch("os.path.exists") as mock_exists,
              patch("src.commands.undo.open") as mock_open):
            mock_exists.return_value = True
            mock_file = mock_open.return_value.__enter__.return_value
            mock_file.readlines.return_value = []
            undo([], [])
            mock_open.assert_called_once_with(UNDO_HISTORY_FILE, "r", encoding="utf-8")
            mock_error.assert_called_once_with("undo", "commands in history", "cp, mv, rm")
            mock_log.assert_not_called()

    def test_cp_file(self):
        with (patch("logging.info") as mock_log,
              patch("os.path.exists") as mock_exists,
              patch("src.commands.undo.open") as mock_open,
              patch("os.path.isfile") as mock_isfile,
              patch("os.path.isdir") as mock_isdir,
              patch("shutil.copy") as mock_copy,
              patch("os.remove") as mock_remove,
              patch("shutil.copytree") as mock_copytree,
              patch("shutil.rmtree") as mock_rmtree, ):
            mock_exists.return_value = True
            mock_isfile.return_value = True
            mock_isdir.return_value = False
            mock_file = mock_open.return_value.__enter__.return_value
            mock_file.readlines.return_value = ["51 cp path1 path2"]
            undo([], [])
            mock_copy.assert_called_once_with(os.path.join(TRASH_DIRECTORY, "51_path2"),
                                              os.path.abspath("path2"))
            mock_copytree.assert_not_called()
            mock_rmtree.assert_not_called()
            self.assertEqual(mock_open.call_count, 2)
            self.assertEqual(mock_open.call_args_list,
                             [call(UNDO_HISTORY_FILE, "r", encoding="utf-8"),
                              call(UNDO_HISTORY_FILE, "w", encoding="utf-8")])
            self.assertEqual(mock_remove.call_count, 2)
            self.assertEqual(mock_remove.call_args_list,
                             [call(os.path.abspath("path2")),
                              call(os.path.join(TRASH_DIRECTORY, "51_path2"))])
            mock_log.assert_called_once_with("Success")

    def test_cp_directory(self):
        with (patch("logging.info") as mock_log,
              patch("os.path.exists") as mock_exists,
              patch("src.commands.undo.open") as mock_open,
              patch("os.path.isfile") as mock_isfile,
              patch("os.path.isdir") as mock_isdir,
              patch("shutil.copy") as mock_copy,
              patch("os.remove") as mock_remove,
              patch("shutil.copytree") as mock_copytree,
              patch("shutil.rmtree") as mock_rmtree, ):
            mock_exists.return_value = True
            mock_isfile.return_value = False
            mock_isdir.return_value = True
            mock_file = mock_open.return_value.__enter__.return_value
            mock_file.readlines.return_value = ["51 cp path1 path2"]
            undo([], [])
            mock_copytree.assert_called_once_with(os.path.join(TRASH_DIRECTORY, "51_path2"),
                                                  os.path.abspath("path2"))
            mock_copy.assert_not_called()
            mock_remove.assert_not_called()
            self.assertEqual(mock_open.call_count, 2)
            self.assertEqual(mock_open.call_args_list,
                             [call(UNDO_HISTORY_FILE, "r", encoding="utf-8"),
                              call(UNDO_HISTORY_FILE, "w", encoding="utf-8")])
            self.assertEqual(mock_rmtree.call_count, 2)
            self.assertEqual(mock_rmtree.call_args_list,
                             [call(os.path.abspath("path2")),
                              call(os.path.join(TRASH_DIRECTORY, "51_path2"))])
            mock_log.assert_called_once_with("Success")

    def test_mv_file(self):
        with (patch("logging.info") as mock_log,
              patch("os.path.exists") as mock_exists,
              patch("src.commands.undo.open") as mock_open,
              patch("os.path.isfile") as mock_isfile,
              patch("os.path.isdir") as mock_isdir,
              patch("shutil.copy") as mock_copy,
              patch("os.remove") as mock_remove,
              patch("shutil.copytree") as mock_copytree,
              patch("shutil.rmtree") as mock_rmtree,
              patch("os.rename") as mock_rename, ):
            mock_exists.return_value = True
            mock_isfile.return_value = True
            mock_isdir.return_value = False
            mock_file = mock_open.return_value.__enter__.return_value
            mock_file.readlines.return_value = ["51 mv path1 path2"]
            undo([], [])
            mock_rename.assert_called_once_with(os.path.abspath("path2"),
                                                os.path.abspath("path1"))
            mock_copy.assert_called_once_with(os.path.join(TRASH_DIRECTORY, "51_path2"),
                                              os.path.abspath("path2"))
            mock_copytree.assert_not_called()
            mock_rmtree.assert_not_called()
            self.assertEqual(mock_open.call_count, 2)
            self.assertEqual(mock_open.call_args_list,
                             [call(UNDO_HISTORY_FILE, "r", encoding="utf-8"),
                              call(UNDO_HISTORY_FILE, "w", encoding="utf-8")])
            mock_remove.assert_called_once_with(os.path.join(TRASH_DIRECTORY, "51_path2"))
            mock_log.assert_called_once_with("Success")

    def test_mv_directory(self):
        with (patch("logging.info") as mock_log,
              patch("os.path.exists") as mock_exists,
              patch("src.commands.undo.open") as mock_open,
              patch("os.path.isfile") as mock_isfile,
              patch("os.path.isdir") as mock_isdir,
              patch("shutil.copy") as mock_copy,
              patch("os.remove") as mock_remove,
              patch("shutil.copytree") as mock_copytree,
              patch("shutil.rmtree") as mock_rmtree,
              patch("os.rename") as mock_rename, ):
            mock_exists.return_value = True
            mock_isfile.return_value = False
            mock_isdir.return_value = True
            mock_file = mock_open.return_value.__enter__.return_value
            mock_file.readlines.return_value = ["51 mv path1 path2"]
            undo([], [])
            mock_rename.assert_called_once_with(os.path.abspath("path2"),
                                                os.path.abspath("path1"))
            mock_copytree.assert_called_once_with(os.path.join(TRASH_DIRECTORY, "51_path2"),
                                                  os.path.abspath("path2"))
            mock_copy.assert_not_called()
            mock_remove.assert_not_called()
            self.assertEqual(mock_open.call_count, 2)
            self.assertEqual(mock_open.call_args_list,
                             [call(UNDO_HISTORY_FILE, "r", encoding="utf-8"),
                              call(UNDO_HISTORY_FILE, "w", encoding="utf-8")])
            mock_rmtree.assert_called_once_with(os.path.join(TRASH_DIRECTORY, "51_path2"))
            mock_log.assert_called_once_with("Success")

    def test_rm_file(self):
        with (patch("logging.info") as mock_log,
              patch("os.path.exists") as mock_exists,
              patch("src.commands.undo.open") as mock_open,
              patch("os.path.isfile") as mock_isfile,
              patch("os.path.isdir") as mock_isdir,
              patch("shutil.copy") as mock_copy,
              patch("os.remove") as mock_remove,
              patch("shutil.copytree") as mock_copytree,
              patch("shutil.rmtree") as mock_rmtree):
            mock_exists.return_value = True
            mock_isfile.return_value = True
            mock_isdir.return_value = False
            mock_file = mock_open.return_value.__enter__.return_value
            mock_file.readlines.return_value = ["51 rm path1"]
            undo([], [])
            mock_copy.assert_called_once_with(os.path.join(TRASH_DIRECTORY, "51_path1"),
                                              os.path.abspath("path1"))
            mock_copytree.assert_not_called()
            mock_rmtree.assert_not_called()
            self.assertEqual(mock_open.call_count, 2)
            self.assertEqual(mock_open.call_args_list,
                             [call(UNDO_HISTORY_FILE, "r", encoding="utf-8"),
                              call(UNDO_HISTORY_FILE, "w", encoding="utf-8")])
            mock_remove.assert_called_once_with(os.path.join(TRASH_DIRECTORY, "51_path1"))
            mock_log.assert_called_once_with("Success")

    def test_rm_directory(self):
        with (patch("logging.info") as mock_log,
              patch("os.path.exists") as mock_exists,
              patch("src.commands.undo.open") as mock_open,
              patch("os.path.isfile") as mock_isfile,
              patch("os.path.isdir") as mock_isdir,
              patch("shutil.copy") as mock_copy,
              patch("os.remove") as mock_remove,
              patch("shutil.copytree") as mock_copytree,
              patch("shutil.rmtree") as mock_rmtree):
            mock_exists.return_value = True
            mock_isfile.return_value = False
            mock_isdir.return_value = True
            mock_file = mock_open.return_value.__enter__.return_value
            mock_file.readlines.return_value = ["51 rm path1"]
            undo([], [])
            mock_copytree.assert_called_once_with(os.path.join(TRASH_DIRECTORY, "51_path1"),
                                                  os.path.abspath("path1"))
            mock_copy.assert_not_called()
            mock_remove.assert_not_called()
            self.assertEqual(mock_open.call_count, 2)
            self.assertEqual(mock_open.call_args_list,
                             [call(UNDO_HISTORY_FILE, "r", encoding="utf-8"),
                              call(UNDO_HISTORY_FILE, "w", encoding="utf-8")])
            mock_rmtree.assert_called_once_with(os.path.join(TRASH_DIRECTORY, "51_path1"))
            mock_log.assert_called_once_with("Success")
