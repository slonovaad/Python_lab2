import unittest
from unittest.mock import patch, call
from src.write_to_history import write_to_history


class WriteToHistoryTestCase(unittest.TestCase):
    """Тесты для функции write_to_history"""

    def test_file_and_history_exists(self):
        with (patch("src.write_to_history.open") as mock_open,
              patch("src.write_to_history.get_command_number") as mock_get_number,
              patch("os.path.exists") as mock_exists):
            mock_exists.return_value = True
            mock_file = mock_open.return_value.__enter__.return_value
            mock_file.readlines.return_value = ["1 ls\n"]
            mock_get_number.return_value = 2
            path = "file"
            input_line = "cd .."
            write_to_history(path, input_line)
            mock_get_number.assert_called_once()
            self.assertEqual(mock_open.call_args_list, [
                call(path, "r", encoding="utf-8"),
                call(path, "w", encoding="utf-8")
            ])
            mock_file.writelines.assert_called_once_with(["1 ls\n", f"2 {input_line}\n"])

    def test_file_and_history_not_exists(self):
        with (patch("src.write_to_history.open") as mock_open,
              patch("src.write_to_history.get_command_number") as mock_get_number,
              patch("os.path.exists") as mock_exists):
            mock_exists.return_value = False
            mock_file = mock_open.return_value.__enter__.return_value
            mock_get_number.return_value = 1
            path = "file"
            input_line = "cd .."
            write_to_history(path, input_line)
            mock_get_number.assert_called_once()
            mock_open.assert_called_once_with(path, "w", encoding="utf-8")
            mock_file.writelines.assert_called_once_with([f"1 {input_line}\n"])
