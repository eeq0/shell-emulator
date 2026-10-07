"""Тесты запуска с параметрами командной строки."""
import contextlib
import io
import os
import tempfile
import unittest

import helpers
from shell import main


def run_main(argv):
    """Запустить main и вернуть (код, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(argv)
    return code, out.getvalue(), err.getvalue()


class CliTest(unittest.TestCase):
    """Проверки параметров --vfs и --script."""

    def setUp(self):
        """Временная папка для скриптов."""
        self.folder = tempfile.TemporaryDirectory()

    def tearDown(self):
        """Удалить временную папку."""
        self.folder.cleanup()

    def write(self, name, text):
        """Записать файл во временную папку и вернуть путь."""
        path = os.path.join(self.folder.name, name)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)
        return path

    def test_debug_output(self):
        """Параметры печатаются при запуске."""
        script = self.write("s.emu", "exit\n")
        _, out, _ = run_main(["--script", script])
        self.assertIn("[debug]   script = " + script, out)

    def test_script_echo_and_skip_errors(self):
        """Скрипт показывает ввод и вывод, ошибочные строки пропускает."""
        script = self.write("s.emu", "ls\nfoo\nls tmp\nexit\n")
        code, out, err = run_main(["--script", script])
        self.assertEqual(code, 0)
        self.assertIn("default:/$ ls", out)
        self.assertIn("foo: команда не найдена", err)
        self.assertIn(":2:", err)

    def test_missing_script(self):
        """Нет скрипта: ошибка и код 1."""
        code, _, err = run_main(["--script", "/no/such/script.emu"])
        self.assertEqual(code, 1)
        self.assertIn("не удалось прочитать скрипт", err)

    def test_bad_vfs(self):
        """Неверная VFS: ошибка и код 1."""
        bad = self.write("bad.zip", "not a zip")
        code, _, err = run_main(["--vfs", bad])
        self.assertEqual(code, 1)
        self.assertIn("неверный формат", err)

    def test_vfs_from_zip(self):
        """VFS из ZIP попадает в приглашение."""
        archive = os.path.join(self.folder.name, "mini.zip")
        helpers.make_zip(archive, {"hello.txt": b"hi"})
        script = self.write("s.emu", "ls\nexit\n")
        _, out, _ = run_main(["--vfs", archive, "--script", script])
        self.assertIn("mini:/$ ls", out)
        self.assertIn("hello.txt", out)


if __name__ == "__main__":
    unittest.main()
