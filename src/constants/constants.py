import os
from pathlib import Path

PROJECT_DIRECTORY = Path(__file__).resolve().parents[2]
LOG_FILE = os.path.join(PROJECT_DIRECTORY, "shell.log")
HISTORY_FILE = os.path.join(PROJECT_DIRECTORY, ".history")
UNDO_HISTORY_FILE = os.path.join(PROJECT_DIRECTORY, ".undo_history")
TRASH_DIRECTORY = os.path.join(PROJECT_DIRECTORY, ".trash")
HISTORY_LIMIT = 20
