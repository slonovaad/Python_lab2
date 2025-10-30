import unittest
from unittest.mock import patch, call
from src.write_to_history import write_to_history
from src.constants.constants import HISTORY_FILE


class WriteToHistoryTestCase(unittest.TestCase):
    """Тесты для функции write_to_history"""

    def test_file_and_history_exists(self):
        with (patch("src.write_to_history.open") as mock_open,
              patch("os.path.exists") as mock_exists):
            mock_exists.return_value = True
            mock_file = mock_open.return_value.__enter__.return_value
            mock_file.readlines.return_value = ["1 ls\n"]
            path = "file"
            input_line = "cd .."
            write_to_history(path, input_line)
            self.assertEqual(mock_open.call_args_list, [
                call(HISTORY_FILE, "r", encoding="utf-8"),
                call(path, "r", encoding="utf-8"),
                call(path, "w", encoding="utf-8")
            ])
            mock_file.writelines.assert_called_once_with(["1 ls\n", f"2 {input_line}\n"])

    def test_file_and_history_not_exists(self):
        with (patch("src.write_to_history.open") as mock_open,
              patch("os.path.exists") as mock_exists):
            mock_exists.return_value = False
            mock_file = mock_open.return_value.__enter__.return_value
            path = "file"
            input_line = "cd .."
            write_to_history(path, input_line)
            mock_open.assert_called_once_with(path, "w", encoding="utf-8")
            mock_file.writelines.assert_called_once_with([f"1 {input_line}\n"])
