"""Ядро эмулятора: выполнение команд, REPL и стартовые скрипты."""
import sys

from commands import COMMANDS
from errors import ShellError, VFSError
from line_parser import parse_line

COMMENT_MARK = "#"


class Shell:
    """Оболочка: хранит текущую VFS и умеет выполнять команды."""

    def __init__(self, vfs, vfs_path=None):
        """vfs: текущая VFS; vfs_path: путь к её ZIP-файлу или None."""
        self.vfs = vfs
        self.vfs_path = vfs_path

    def prompt(self):
        """Приглашение к вводу: имя VFS и текущий каталог."""
        return f"{self.vfs.name}:{self.vfs.cwd_path()}$ "

    def execute(self, line):
        """Выполнить одну строку. Ошибки приходят как ShellError."""
        words = parse_line(line)
        if not words:
            return
        name, args = words[0], words[1:]
        handler = COMMANDS.get(name)
        if handler is None:
            raise ShellError(f"{name}: команда не найдена")
        try:
            handler(self, args)
        except VFSError as err:
            raise ShellError(f"{name}: {err}") from err

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
