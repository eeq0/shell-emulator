"""Ядро эмулятора: выполнение команд и интерактивный цикл (REPL)."""
import sys

from commands import COMMANDS
from errors import ShellError
from line_parser import parse_line

VFS_NAME = "default"


class Shell:
    """Оболочка: умеет выполнять команды."""

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
