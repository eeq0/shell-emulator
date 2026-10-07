"""Тесты команд оболочки."""
import os
import tempfile
import unittest
from datetime import date

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

    def test_ls(self):
        """ls показывает каталоги со слешем."""
        self.assertEqual(self.run_line("ls").strip(), "etc/  home/  tmp/")

    def test_ls_path_and_file(self):
        """ls с путём к каталогу и к файлу."""
        self.assertEqual(self.run_line("ls home"), "user/\n")
        self.assertEqual(self.run_line("ls etc/hostname"), "hostname\n")

    def test_cd_changes_prompt(self):
        """После cd меняется приглашение."""
        self.run_line("cd home/user")
        self.assertEqual(self.shell.prompt(), "default:/home/user$ ")
        self.run_line("cd ..")
        self.assertEqual(self.shell.prompt(), "default:/home$ ")

    def test_cal_month_year(self):
        """cal с месяцем и годом."""
        self.assertIn("February 2024", self.run_line("cal 2 2024"))

    def test_cal_current_month(self):
        """cal без аргументов показывает текущий месяц."""
        today = date.today()
        self.assertIn(str(today.year), self.run_line("cal"))

    def test_date(self):
        """date печатает текущий год."""
        self.assertIn(str(date.today().year), self.run_line("date"))

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

    def test_mv_rmdir_only_in_memory(self):
        """mv и rmdir меняют VFS в памяти, а ZIP на диске остаётся прежним."""
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "disk.zip")
            helpers.make_zip(path, {"a.txt": b"a", "empty/": b""})
            with open(path, "rb") as handle:
                before = handle.read()
            self.shell = Shell(load_zip(path), path)
            self.run_line("mv a.txt b.txt")
            self.run_line("rmdir empty")
            self.assertEqual(self.run_line("ls"), "b.txt\n")
            with open(path, "rb") as handle:
                self.assertEqual(handle.read(), before)

    def test_errors(self):
        """Неизвестная команда и неверные аргументы."""
        for line in ["foo", "cd a b", "ls a b", "cal 13 2024",
                     "cal 2026", "date x", "mv a", "rmdir", "exit 1"]:
            with self.assertRaises(ShellError, msg=line):
                self.run_line(line)

    def test_exit(self):
        """exit завершает программу."""
        with self.assertRaises(SystemExit):
            self.run_line("exit")


if __name__ == "__main__":
    unittest.main()
