"""Команды эмулятора. Каждая получает оболочку и список аргументов."""
from errors import ShellError

CD_MAX_ARGS = 1


def cmd_ls(shell, args):
    """ls: заглушка, печатает имя команды и аргументы."""
    print(" ".join(["ls"] + args))


def cmd_cd(shell, args):
    """cd: заглушка, печатает имя команды и аргументы."""
    if len(args) > CD_MAX_ARGS:
        raise ShellError("cd: слишком много аргументов")
    print(" ".join(["cd"] + args))


def cmd_exit(shell, args):
    """exit: завершить работу эмулятора."""
    if args:
        raise ShellError("exit: команда не принимает аргументов")
    raise SystemExit(0)


COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "exit": cmd_exit,
}
