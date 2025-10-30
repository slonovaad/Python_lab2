import unittest
from src.parse import parse


class ParseTestCase(unittest.TestCase):
    """Тесты для функции parse"""

    def test_without_options(self):
        result = parse("cd directory")
        self.assertEqual(result, ("cd", [], ["directory"]))

    def test_without_path(self):
        result = parse("ls -l")
        self.assertEqual(result, ("ls", ["-l"], []))

    def test_only_command(self):
        result = parse("ls")
        self.assertEqual(result, ("ls", [], []))

    def test_with_options(self):
        result = parse("ls -l directory")
        self.assertEqual(result, ("ls", ["-l"], ["directory"]))

    def test_double_option(self):
        result = parse("ls -l -l directory")
        self.assertEqual(result, ("ls", ["-l"], ["directory"]))

    def test_with_many_paths(self):
        result = parse("cp -r directory1 directory2")
        self.assertEqual(result, ("cp", ["-r"], ["directory1", "directory2"]))

    def test_with_spaces(self):
        result = parse('cp -r directory1 "directory 2"')
        self.assertEqual(result, ("cp", ["-r"], ["directory1", "directory 2"]))

    def test_with_many_options(self):
        result = parse("grep -r -i pattern path")
        self.assertEqual(result, ("grep", ["-r", "-i"], ["pattern", "path"]))

    def test_with_many_options_on_one(self):
        result = parse("grep -ri pattern path")
        self.assertEqual(result, ("grep", ["-r", "-i"], ["pattern", "path"]))

    def test_double_minus(self):
        result = parse("grep --r pattern path")
        self.assertEqual(result, ("grep", ["-r"], ["pattern", "path"]))

    def test_minuses_in_path(self):
        result = parse("ls -l -diretory--path-1-b")
        self.assertEqual(result, ("ls", ["-l"], ["-diretory--path-1-b"]))

    def test_minuses_and_spaces_in_path(self):
        result = parse('ls -l "-diretory--path-1 -b"')
        self.assertEqual(result, ("ls", ["-l"], ["-diretory--path-1 -b"]))

    def test_option_in_middle(self):
        result = parse("grep -i pattern -r directory_path")
        self.assertEqual(result, ("grep", ["-i", "-r"], ["pattern", "directory_path"]))

    def test_option_in_end(self):
        result = parse("grep -i pattern directory_path -r")
        self.assertEqual(result, ("grep", ["-i", "-r"], ["pattern", "directory_path"]))
