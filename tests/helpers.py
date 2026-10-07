"""Общие вспомогательные функции для тестов."""
import contextlib
import io
import os
import sys
import zipfile

SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
sys.path.insert(0, SRC_DIR)


def make_zip(path, files):
    """Создать ZIP-архив из словаря «имя -> байты»."""
    with zipfile.ZipFile(path, "w") as archive:
        for name, data in files.items():
            archive.writestr(name, data)


def run_line(shell, line):
    """Выполнить строку в оболочке и вернуть всё, что она напечатала."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        shell.execute(line)
    return buffer.getvalue()
