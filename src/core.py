"""Ядро эмулятора: выполнение команд и интерактивный цикл (REPL)."""
import sys

from commands import COMMANDS
from errors import ShellError
from line_parser import parse_line

VFS_NAME = "default"
COMMENT_MARK = "#"


class Shell:
    """Оболочка: умеет выполнять команды."""

    def __init__(self, vfs_path=None):
        """vfs_path: путь к VFS из параметра --vfs (пока не загружается)."""
        self.vfs_path = vfs_path

    def prompt(self):
        """Приглашение к вводу с именем VFS."""
        return f"{VFS_NAME}$ "

    def execute(self, line):
        """Выполнить одну строку. Ошибки приходят как ShellError."""
        words = parse_line(line)
        if not words:
            return
        name, args = words[0], words[1:]
        handler = COMMANDS.get(name)
        if handler is None:
            raise ShellError(f"{name}: команда не найдена")
        handler(self, args)

    def repl(self):
        """Интерактивный цикл: прочитать строку, выполнить, повторить."""
        while True:
            try:
                line = input(self.prompt())
            except EOFError:
                print()
                return
            except KeyboardInterrupt:
                print()
                continue
            try:
                self.execute(line)
            except ShellError as err:
                print(err, file=sys.stderr)

    def run_script(self, path):
        """Выполнить стартовый скрипт, показывая и ввод, и вывод."""
        try:
            with open(path, encoding="utf-8") as handle:
                lines = handle.read().splitlines()
        except (OSError, UnicodeError) as err:
            raise ShellError(f"не удалось прочитать скрипт {path}") from err
        for number, line in enumerate(lines, start=1):
            self._run_script_line(path, number, line)

    def _run_script_line(self, path, number, line):
        """Выполнить одну строку скрипта; ошибочную пропустить."""
        text = line.strip()
        if not text:
            return
        if text.startswith(COMMENT_MARK):
            print(text)
            return
        print(self.prompt() + text)
        try:
            self.execute(text)
        except ShellError as err:
            print(f"{path}:{number}: {err}", file=sys.stderr)
