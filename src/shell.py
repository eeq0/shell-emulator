"""Точка входа эмулятора оболочки: python3 src/shell.py [параметры]."""
import argparse
import sys

from core import Shell
from errors import ShellError
from vfs import default_vfs, load_zip

EXIT_ERROR = 1


def build_arg_parser():
    """Описать параметры командной строки."""
    parser = argparse.ArgumentParser(description="Эмулятор оболочки UNIX")
    parser.add_argument("--vfs", metavar="PATH",
                        help="путь к ZIP-архиву с VFS")
    parser.add_argument("--script", metavar="PATH",
                        help="путь к стартовому скрипту")
    return parser


def print_debug(args):
    """Отладочный вывод всех заданных параметров."""
    print("[debug] параметры запуска:")
    print(f"[debug]   vfs    = {args.vfs}")
    print(f"[debug]   script = {args.script}")


def start(args):
    """Загрузить VFS, выполнить скрипт и запустить REPL."""
    vfs = load_zip(args.vfs) if args.vfs else default_vfs()
    shell = Shell(vfs, args.vfs)
    if args.script:
        shell.run_script(args.script)
    shell.repl()


def main(argv=None):
    """Запустить эмулятор и вернуть код завершения."""
    args = build_arg_parser().parse_args(argv)
    print_debug(args)
    try:
        start(args)
    except SystemExit as stop:
        return stop.code
    except ShellError as err:
        print(f"ошибка: {err}", file=sys.stderr)
        return EXIT_ERROR
    return 0


if __name__ == "__main__":
    sys.exit(main())
