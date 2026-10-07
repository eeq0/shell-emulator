#!/bin/sh
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
python3 "$ROOT/scripts/make_vfs.py" "$TMP"
EMU="sh $ROOT/run.sh"
START="$ROOT/examples/stage3_vfs.emu"

for name in minimal files deep; do
    echo "=== VFS загружается: $name.zip"
    echo "exit" | $EMU --vfs "$TMP/$name.zip"
done

echo "=== ошибка: файл не является ZIP"
$EMU --vfs "$TMP/bad.zip"
echo "код возврата: $?"

echo "=== ошибка: файла нет"
$EMU --vfs "$TMP/missing.zip"
echo "код возврата: $?"

echo "=== ошибка: вместо файла указана папка"
$EMU --vfs "$TMP"
echo "код возврата: $?"

rm -rf "$TMP"
