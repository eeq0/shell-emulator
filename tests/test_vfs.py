"""Тесты загрузки VFS из ZIP."""
import os
import tempfile
import unittest

import helpers
from errors import VFSError
from vfs import Dir, default_vfs, load_zip, save_zip

FILES = {
    "a.txt": b"abc",
    "bin.dat": bytes([0, 255, 7]),
    "docs/work/todo.txt": b"x",
    "docs/empty/": b"",
}


class LoadZipTest(unittest.TestCase):
    """Загрузка VFS из ZIP."""

    def setUp(self):
        """Создать временный архив."""
        self.folder = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.folder.name, "sample.zip")
        helpers.make_zip(self.path, FILES)

    def tearDown(self):
        """Удалить временную папку."""
        self.folder.cleanup()

    def test_structure_and_name(self):
        """Дерево собрано, имя VFS взято из имени файла."""
        vfs = load_zip(self.path)
        docs = vfs.root.children["docs"]
        self.assertEqual(vfs.name, "sample")
        self.assertIsInstance(docs.children["work"], Dir)
        self.assertIsInstance(docs.children["empty"], Dir)

    def test_binary_size(self):
        """Бинарные данные хранятся без потерь (через base64)."""
        vfs = load_zip(self.path)
        self.assertEqual(vfs.root.children["bin.dat"].size(), 3)

    def test_missing_file(self):
        """Нет файла: ошибка загрузки."""
        with self.assertRaises(VFSError):
            load_zip(os.path.join(self.folder.name, "none.zip"))

    def test_bad_format(self):
        """Не ZIP: ошибка загрузки."""
        bad = os.path.join(self.folder.name, "bad.zip")
        with open(bad, "w", encoding="utf-8") as handle:
            handle.write("not a zip")
        with self.assertRaises(VFSError):
            load_zip(bad)


class SaveZipTest(unittest.TestCase):
    """Запись VFS в ZIP-архив."""

    def test_round_trip(self):
        """Записанную VFS можно загрузить обратно без потерь."""
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "out.zip")
            save_zip(default_vfs(), path)
            vfs = load_zip(path)
            user = vfs.root.children["home"].children["user"]
            self.assertEqual(user.children["notes.txt"].size(), 6)
            self.assertEqual(vfs.root.children["tmp"].children, {})


if __name__ == "__main__":
    unittest.main()
