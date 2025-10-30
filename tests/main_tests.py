import unittest
from unittest.mock import patch, call
from src.main import main
from src.constants.constants import UNDO_HISTORY_FILE, TRASH_DIRECTORY, HISTORY_FILE


class MainTestCase(unittest.TestCase):
    """Тесты для функции main"""

    def test_blank_line(self):
        with (patch("src.main.input") as mock_input,
              patch("logging.info") as mock_log,
              patch("src.main.write_to_history") as mock_history,
              patch("os.path.exists") as mock_exists,
              patch("os.remove") as mock_remove,
              patch("shutil.rmtree") as mock_rmtree, ):
            input_str = ""
            mock_input.side_effect = [input_str, "exit"]
            mock_exists.return_value = True
            main()
            self.assertEqual(mock_input.call_count, 2)
            self.assertEqual(mock_log.call_count, 4)
            self.assertEqual(mock_log.call_args_list, [
                call(input_str), call("Blank line"),
                call("exit"), call("Exit")])
            mock_remove.assert_called_once_with(UNDO_HISTORY_FILE)
            mock_rmtree.assert_called_once_with(TRASH_DIRECTORY)
            mock_history.assert_called_once_with(HISTORY_FILE, "exit")

    @patch.dict("src.main.COMMANDS", {"ls": lambda x, y: ""})
    def test_any_command(self):
        with (patch("src.main.input") as mock_input,
              patch("logging.info") as mock_log,
              patch("src.main.write_to_history") as mock_history,
              patch("os.path.exists") as mock_exists,
              patch("os.remove") as mock_remove,
              patch("shutil.rmtree") as mock_rmtree):
            input_str = "ls"
            mock_input.side_effect = [input_str, "exit"]
            mock_exists.return_value = True
            main()
            self.assertEqual(mock_input.call_count, 2)
            self.assertEqual(mock_log.call_args_list, [
                call(input_str),
                call("exit"), call("Exit")])
            mock_remove.assert_called_once_with(UNDO_HISTORY_FILE)
            mock_rmtree.assert_called_once_with(TRASH_DIRECTORY)
            self.assertEqual(mock_history.call_args_list, [
                call(HISTORY_FILE, input_str), call(HISTORY_FILE, "exit")])

    @patch.dict("src.main.COMMANDS", {"ls": lambda x, y: ""})
    def test_command_not_found(self):
        with (patch("src.main.input") as mock_input,
              patch("logging.info") as mock_log,
              patch("src.main.command_not_found_error_message") as mock_error,
              patch("src.main.write_to_history") as mock_history,
              patch("os.path.exists") as mock_exists,
              patch("os.remove") as mock_remove,
              patch("shutil.rmtree") as mock_rmtree):
            input_str = "somecommand -l"
            mock_input.side_effect = [input_str, "exit"]
            mock_exists.return_value = True
            main()
            self.assertEqual(mock_input.call_count, 2)
            self.assertEqual(mock_log.call_args_list, [
                call(input_str),
                call("exit"), call("Exit")])
            mock_error.assert_called_once_with("somecommand")
            mock_remove.assert_called_once_with(UNDO_HISTORY_FILE)
            mock_rmtree.assert_called_once_with(TRASH_DIRECTORY)
            self.assertEqual(mock_history.call_args_list, [
                call(HISTORY_FILE, input_str), call(HISTORY_FILE, "exit")])
