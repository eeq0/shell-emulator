"""Виртуальная файловая система (VFS), которая целиком живёт в памяти."""
import base64
import os
import zipfile
import zlib

from errors import VFSError

DEFAULT_VFS_NAME = "default"
PARENT = ".."
CURRENT = "."
SEPARATOR = "/"
DEFAULT_TREE = {
    "home": {"user": {"notes.txt": "hello\n"}},
    "etc": {"hostname": "emulator\n"},
    "tmp": {},
}


class File:
    """Файл. Данные хранятся в base64, поэтому подходят и бинарные."""

    mark = "-"
    suffix = ""

    def __init__(self, data_b64):
        """Создать файл из строки base64."""
        self.data_b64 = data_b64

    @classmethod
    def from_bytes(cls, data):
        """Создать файл из обычных байтов."""
        return cls(base64.b64encode(data).decode("ascii"))

    def size(self):
        """Размер файла в байтах."""
        return len(base64.b64decode(self.data_b64))


class Dir:
    """Каталог: словарь «имя -> файл или каталог»."""

    mark = "d"
    suffix = SEPARATOR

    def __init__(self):
        """Создать пустой каталог."""
        self.children = {}

    def size(self):
        """У каталога размер всегда 0."""
        return 0


class VFS:
    """Дерево каталогов и файлов плюс текущий каталог (cwd)."""

    def __init__(self, name, root):
        """Создать VFS с именем name и корневым каталогом root."""
        self.name = name
        self.root = root
        self.cwd = []

    def cwd_path(self):
        """Текущий каталог в виде строки, например '/docs/work'."""
        return SEPARATOR + SEPARATOR.join(self.cwd)


def _build_dir(tree):
    """Построить каталог из вложенных словарей (текст -> файл)."""
    directory = Dir()
    for name, value in tree.items():
        if isinstance(value, dict):
            directory.children[name] = _build_dir(value)
        else:
            directory.children[name] = File.from_bytes(value.encode())
    return directory


def default_vfs():
    """VFS по умолчанию, которая встроена в программу."""
    return VFS(DEFAULT_VFS_NAME, _build_dir(DEFAULT_TREE))


def _ensure_dir(parent, name):
    """Вернуть подкаталог name, создав его при необходимости."""
    child = parent.children.setdefault(name, Dir())
    if not isinstance(child, Dir):
        raise VFSError(f"в архиве '{name}' и файл, и каталог")
    return child


def _add_entry(root, info, archive):
    """Добавить одну запись ZIP-архива в дерево VFS."""
    skipped = ("", CURRENT)
    parts = [p for p in info.filename.split(SEPARATOR) if p not in skipped]
    if PARENT in parts:
        raise VFSError(f"небезопасный путь в архиве: {info.filename}")
    if not parts:
        return
    parent = root
    for name in parts[:-1]:
        parent = _ensure_dir(parent, name)
    if info.is_dir():
        _ensure_dir(parent, parts[-1])
    else:
        parent.children[parts[-1]] = File.from_bytes(archive.read(info))


def _read_archive(archive):
    """Прочитать весь архив в память и вернуть корневой каталог."""
    root = Dir()
    for info in archive.infolist():
        _add_entry(root, info, archive)
    return root


def load_zip(path):
    """Загрузить VFS из ZIP-архива. Распаковки на диск нет."""
    try:
        with zipfile.ZipFile(path) as archive:
            root = _read_archive(archive)
    except FileNotFoundError as err:
        raise VFSError(f"файл не найден: {path}") from err
    except (zipfile.BadZipFile, zlib.error, RuntimeError,
            NotImplementedError) as err:
        raise VFSError(f"неверный формат (нужен ZIP): {path}") from err
    except OSError as err:
        raise VFSError(f"не удалось открыть {path}: {err.strerror}") from err
    stem = os.path.splitext(os.path.basename(path))[0]
    return VFS(stem or DEFAULT_VFS_NAME, root)


def _write_dir(archive, directory, prefix):
    """Записать содержимое каталога в открытый ZIP-архив."""
    for name, node in sorted(directory.children.items()):
        path = prefix + name
        if isinstance(node, Dir):
            archive.writestr(path + SEPARATOR, b"")
            _write_dir(archive, node, path + SEPARATOR)
        else:
            archive.writestr(path, base64.b64decode(node.data_b64))


def save_zip(vfs, path):
    """Записать VFS в ZIP-архив, полностью заменив его прежнее содержимое."""
    try:
        with zipfile.ZipFile(path, "w") as archive:
            _write_dir(archive, vfs.root, "")
    except OSError as err:
        raise VFSError(f"не удалось записать {path}: {err.strerror}") from err
