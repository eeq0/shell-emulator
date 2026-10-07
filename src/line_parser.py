"""Разбор введённой строки на слова."""
import os
import shlex

from errors import ShellError


def parse_line(line):
    """Разбить строку на слова и раскрыть переменные окружения.

    Кавычки учитываются: 'ls "my dir"' даёт ['ls', 'my dir'].
    Переменные раскрываются из реальной ОС: '$HOME' -> '/Users/me'.
    """
    try:
        words = shlex.split(line)
    except ValueError as err:
        raise ShellError("ошибка разбора: незакрытая кавычка") from err
    return [os.path.expandvars(word) for word in words]
