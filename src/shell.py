"""Точка входа эмулятора оболочки: python3 src/shell.py."""
import sys

from core import Shell


def main():
    """Запустить REPL и вернуть код завершения."""
    try:
        Shell().repl()
    except SystemExit as stop:
        return stop.code
    return 0


if __name__ == "__main__":
    sys.exit(main())
