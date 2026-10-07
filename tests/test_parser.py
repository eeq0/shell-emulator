"""Тесты разбора строки."""
import os
import unittest

import helpers
from errors import ShellError
from line_parser import parse_line


class ParseLineTest(unittest.TestCase):
    """Проверки parse_line."""

    def test_words(self):
        """Строка делится на слова."""
        self.assertEqual(parse_line("ls -l /tmp"), ["ls", "-l", "/tmp"])

    def test_quotes(self):
        """Кавычки склеивают слова."""
        self.assertEqual(parse_line('ls "my dir"'), ["ls", "my dir"])

    def test_env_variable(self):
        """Переменные окружения раскрываются."""
        os.environ["EMU_TEST_VAR"] = "/tmp/x"
        self.assertEqual(parse_line("cd $EMU_TEST_VAR"), ["cd", "/tmp/x"])

    def test_empty(self):
        """Пустая строка даёт пустой список."""
        self.assertEqual(parse_line("   "), [])

    def test_unclosed_quote(self):
        """Незакрытая кавычка это ошибка."""
        with self.assertRaises(ShellError):
            parse_line('ls "oops')


if __name__ == "__main__":
    unittest.main()
