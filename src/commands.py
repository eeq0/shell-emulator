"""Команды эмулятора. Каждая получает оболочку и список аргументов."""
from errors import ShellError
from vfs import save_zip, default_vfs

CD_MAX_ARGS = 1


def cmd_ls(shell, args):
    """ls: заглушка, печатает имя команды и аргументы."""
    print(" ".join(["ls"] + args))


def cmd_cd(shell, args):
    """cd: заглушка, печатает имя команды и аргументы."""
    if len(args) > CD_MAX_ARGS:
        raise ShellError("cd: слишком много аргументов")
    print(" ".join(["cd"] + args))


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
    "vfs-init": cmd_vfs_init,
    "exit": cmd_exit,
}
