"""Создаёт тестовые ZIP-архивы VFS в указанной папке.

Использование: python3 scripts/make_vfs.py ПАПКА
Архивы не хранятся в репозитории, их создают скрипты проверки.
"""
import os
import sys
import zipfile

BINARY_DATA = bytes([0, 1, 2, 254, 255])
ARG_COUNT = 1

VARIANTS = {
    "minimal.zip": {"hello.txt": b"hello\n"},
    "files.zip": {
        "a.txt": b"first\n",
        "b.txt": b"second file\n",
        "image.bin": BINARY_DATA,
    },
    "deep.zip": {
        "readme.txt": b"deep vfs\n",
        "docs/notes.txt": b"notes\n",
        "docs/empty/": b"",
        "docs/work/todo.txt": b"todo\n",
        "docs/work/reports/2026/q3.txt": b"report\n",
        "bin/tool.bin": BINARY_DATA,
    },
}


def write_zip(path, files):
    """Записать ZIP-архив из словаря «имя -> байты»."""
    with zipfile.ZipFile(path, "w") as archive:
        for name, data in files.items():
            archive.writestr(name, data)


def main(argv):
    """Создать все варианты VFS и один заведомо неверный файл."""
    if len(argv) != ARG_COUNT:
        print("использование: make_vfs.py ПАПКА", file=sys.stderr)
        return 1
    folder = argv[0]
    os.makedirs(folder, exist_ok=True)
    for name, files in VARIANTS.items():
        write_zip(os.path.join(folder, name), files)
    with open(os.path.join(folder, "bad.zip"), "w", encoding="utf-8") as bad:
        bad.write("это не ZIP-архив\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
