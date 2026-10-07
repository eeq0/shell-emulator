#!/bin/sh
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
EMU="sh $ROOT/run.sh"
START="$ROOT/examples/stage2_startup.emu"
VFS="$TMP/vfs.zip"

echo "=== ошибка: скрипт не найден"
$EMU --vfs "$VFS" --script "$TMP/no_such.emu"
echo "код возврата: $?"

echo "=== ошибка: неизвестный параметр"
$EMU --bogus
echo "код возврата: $?"

echo "=== ошибка: у --script нет значения"
$EMU --vfs "$VFS" --script
echo "код возврата: $?"

echo "=== для сравнения: оба параметра заданы верно"
$EMU --vfs "$VFS" --script "$START"

rm -rf "$TMP"
