"""Команды эмулятора. Каждая получает оболочку и список аргументов."""
import calendar
from datetime import date, datetime

from errors import ShellError
from vfs import Dir, default_vfs, save_zip

CURRENT_DIR = "."
ROOT_PATH = "/"
SEPARATOR = "/"
LS_MAX_ARGS = 1
CD_MAX_ARGS = 1
CAL_ARG_COUNT = 2
MIN_MONTH = 1
MAX_MONTH = 12
MIN_YEAR = 1
MAX_YEAR = 9999
DATE_FORMAT = "%a %b %e %H:%M:%S %Z %Y"


def _ls_names(node, path):
    """Имена для вывода ls: содержимое каталога или имя файла."""
    if isinstance(node, Dir):
        children = sorted(node.children.items())
        return [name + child.suffix for name, child in children]
    return [path.rstrip(SEPARATOR).split(SEPARATOR)[-1]]


def cmd_ls(shell, args):
    """ls [путь]: показать содержимое каталога (по умолчанию текущего)."""
    if len(args) > LS_MAX_ARGS:
        raise ShellError("ls: слишком много аргументов")
    path = args[0] if args else CURRENT_DIR
    names = _ls_names(shell.vfs.lookup(path), path)
    if names:
        print("  ".join(names))


def cmd_cd(shell, args):
    """cd [путь]: перейти в каталог (без аргумента: в корень)."""
    if len(args) > CD_MAX_ARGS:
        raise ShellError("cd: слишком много аргументов")
    shell.vfs.change_dir(args[0] if args else ROOT_PATH)


def _month_and_year(args):
    """Прочитать месяц и год из аргументов cal и проверить их."""
    if len(args) != CAL_ARG_COUNT:
        raise ShellError("cal: нужно указать месяц и год, например: cal 2 2024")
    try:
        month, year = int(args[0]), int(args[1])
    except ValueError as err:
        raise ShellError("cal: месяц и год должны быть числами") from err
    if not MIN_MONTH <= month <= MAX_MONTH:
        raise ShellError(f"cal: неверный месяц: {month}")
    if not MIN_YEAR <= year <= MAX_YEAR:
        raise ShellError(f"cal: неверный год: {year}")
    return month, year


def cmd_cal(shell, args):
    """cal [месяц год]: показать календарь (по умолчанию текущий месяц)."""
    if args:
        month, year = _month_and_year(args)
    else:
        today = date.today()
        month, year = today.month, today.year
    text = calendar.TextCalendar(calendar.SUNDAY).formatmonth(year, month)
    print(text.rstrip())


def cmd_date(shell, args):
    """date: показать текущие дату и время."""
    if args:
        raise ShellError("date: команда не принимает аргументов")
    print(datetime.now().astimezone().strftime(DATE_FORMAT))


def cmd_vfs_init(shell, args):
    """vfs-init: заменить VFS на VFS по умолчанию.

    Физическое представление (ZIP-файл) тоже очищается: в него
    записывается VFS по умолчанию. Это единственная служебная
    команда, которая меняет файл VFS на диске.
    """
    if args:
        raise ShellError("vfs-init: команда не принимает аргументов")
    shell.vfs = default_vfs()
    if shell.vfs_path:
        save_zip(shell.vfs, shell.vfs_path)
        print(f"VFS заменена на VFS по умолчанию, {shell.vfs_path} очищен")
    else:
        print("VFS заменена на VFS по умолчанию")


def cmd_exit(shell, args):
    """exit: завершить работу эмулятора."""
    if args:
        raise ShellError("exit: команда не принимает аргументов")
    raise SystemExit(0)


COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "cal": cmd_cal,
    "date": cmd_date,
    "vfs-init": cmd_vfs_init,
    "exit": cmd_exit,
}
