"""Тесты команд оболочки (этапы 1 и 2)."""
import os
import unittest

import helpers
from core import Shell
from errors import ShellError


class CommandsTest(unittest.TestCase):
    """Проверки команд-заглушек через Shell.execute."""

    def setUp(self):
        """Новая оболочка для каждого теста."""
        self.shell = Shell()

    def run_line(self, line):
        """Выполнить строку и вернуть вывод."""
        return helpers.run_line(self.shell, line)

    def test_prompt_has_vfs_name(self):
        """В приглашении есть имя VFS."""
        self.assertEqual(self.shell.prompt(), "default$ ")

    def test_ls_stub(self):
        """ls печатает своё имя и аргументы."""
        self.assertEqual(self.run_line("ls /tmp -l"), "ls /tmp -l\n")

    def test_cd_stub(self):
        """cd печатает своё имя и аргумент."""
        self.assertEqual(self.run_line("cd docs"), "cd docs\n")

    def test_env_expansion(self):
        """Переменные окружения раскрываются до выполнения команды."""
        os.environ["EMU_TEST_VAR"] = "/tmp/x"
        self.assertEqual(self.run_line("ls $EMU_TEST_VAR"), "ls /tmp/x\n")

    def test_empty_line(self):
        """Пустая строка ничего не делает."""
        self.assertEqual(self.run_line("   "), "")

    def test_errors(self):
        """Неизвестная команда и неверные аргументы."""
        for line in ["foo", "cd a b", "exit 1"]:
            with self.assertRaises(ShellError, msg=line):
                self.run_line(line)

    def test_exit(self):
        """exit завершает программу."""
        with self.assertRaises(SystemExit):
            self.run_line("exit")


if __name__ == "__main__":
    unittest.main()
