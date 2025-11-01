import unittest
from unittest.mock import patch
from src.get_command_number import get_command_number
from src.constants.constants import HISTORY_FILE


class GetCommandNumberTestCase(unittest.TestCase):
    """Тесты для функции get_command_number"""

    def test_history_file_exists_have_lines(self):
        with (patch("src.get_command_number.open") as mock_open,
              patch("os.path.exists") as mock_exists):
            mock_file = mock_open.return_value.__enter__.return_value
            mock_file.readlines.return_value = ["1 ls\n", "2 cd path1\n", "3 ls -l path2\n"]
            mock_exists.return_value = True
            number = get_command_number()
            mock_open.assert_called_with(HISTORY_FILE, "r", encoding="utf-8")
            self.assertEqual(number, 4)

    def test_history_file_exists_dont_have_lines(self):
        with (patch("src.get_command_number.open") as mock_open,
              patch("os.path.exists") as mock_exists):
            mock_file = mock_open.return_value.__enter__.return_value
            mock_file.readlines.return_value = []
            mock_exists.return_value = True
            number = get_command_number()
            mock_open.assert_called_with(HISTORY_FILE, "r", encoding="utf-8")
            self.assertEqual(number, 1)

    def test_history_file_not_exists(self):
        with (patch("src.get_command_number.open") as mock_open,
              patch("os.path.exists") as mock_exists):
            mock_file = mock_open.return_value.__enter__.return_value
            mock_file.readlines.return_value = []
            mock_exists.return_value = False
            number = get_command_number()
            mock_open.assert_not_called()
            self.assertEqual(number, 1)
