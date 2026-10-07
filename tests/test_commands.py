"""Тесты команд оболочки (этап 3)."""
import os
import tempfile
import unittest

import helpers
from core import Shell
from errors import ShellError
from vfs import default_vfs, load_zip


class CommandsTest(unittest.TestCase):
    """Проверки команд через Shell.execute."""

    def setUp(self):
        """Оболочка с VFS по умолчанию."""
        self.shell = Shell(default_vfs())

    def run_line(self, line):
        """Выполнить строку и вернуть вывод."""
        return helpers.run_line(self.shell, line)

    def test_prompt_has_vfs_name(self):
        """В приглашении есть имя VFS."""
        self.assertEqual(self.shell.prompt(), "default:/$ ")

    def test_stubs(self):
        """ls и cd пока заглушки."""
        self.assertEqual(self.run_line("ls /tmp"), "ls /tmp\n")
        self.assertEqual(self.run_line("cd docs"), "cd docs\n")

    def test_vfs_init_resets(self):
        """vfs-init возвращает VFS по умолчанию и очищает ZIP на диске."""
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "old.zip")
            helpers.make_zip(path, {"old.txt": b"old"})
            self.shell = Shell(load_zip(path), path)
            self.run_line("vfs-init")
            self.assertEqual(self.shell.vfs.name, "default")
            names = load_zip(path).root.children
            self.assertNotIn("old.txt", names)
            self.assertIn("home", names)

    def test_vfs_init_without_file(self):
        """Без ZIP-файла vfs-init меняет VFS только в памяти."""
        self.shell.vfs.name = "other"
        self.run_line("vfs-init")
        self.assertEqual(self.shell.vfs.name, "default")
        self.assertIsNone(self.shell.vfs_path)

    def test_errors(self):
        """Неизвестная команда и неверные аргументы."""
        for line in ["foo", "cd a b", "vfs-init x", "exit 1"]:
            with self.assertRaises(ShellError, msg=line):
                self.run_line(line)

    def test_exit(self):
        """exit завершает программу."""
        with self.assertRaises(SystemExit):
            self.run_line("exit")


if __name__ == "__main__":
    unittest.main()
