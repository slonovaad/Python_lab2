import unittest
from unittest.mock import patch
from src.commands.history import history
from src.constants.constants import HISTORY_FILE


class HistoryTestCase(unittest.TestCase):
    """Тесты для команы history"""

    def test_dont_have_arguments(self):
        with (patch("logging.info") as mock_log,
              patch("src.commands.history.open") as mock_open):
            history([], [])
            mock_open.assert_called_once_with(HISTORY_FILE, "r", encoding="utf-8")
            mock_log.assert_called_once_with("Success")

    def test_one_argument(self):
        with (patch("logging.info") as mock_log,
              patch("src.commands.history.open") as mock_open):
            history([], ["1"])
            mock_open.assert_called_once_with(HISTORY_FILE, "r", encoding="utf-8")
            mock_log.assert_called_once_with("Success")

    def test_more_than_one_argument(self):
        with (patch("src.commands.history.invalid_arguments_error_message") as mock_error,
              patch("src.commands.history.open") as mock_open):
            history([], ["1", "2"])
            mock_open.assert_not_called()
            mock_error.assert_called_once_with("history")

    def test_have_option(self):
        with (patch("src.commands.history.invalid_arguments_error_message") as mock_error,
              patch("src.commands.history.open") as mock_open):
            history(["-l"], ["1"])
            mock_open.assert_not_called()
            mock_error.assert_called_once_with("history")

    def test_not_number_argument(self):
        with (patch("src.commands.history.invalid_arguments_error_message") as mock_error,
              patch("src.commands.history.open") as mock_open):
            history([], ["aa"])
            mock_open.assert_called_once_with(HISTORY_FILE, "r", encoding="utf-8")
            mock_error.assert_called_once_with("history")
