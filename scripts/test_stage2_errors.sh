#!/bin/sh
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
python3 "$ROOT/scripts/make_vfs.py" "$TMP"
EMU="sh $ROOT/run.sh"
START="$ROOT/examples/stage2_startup.emu"

echo "=== ошибка: скрипт не найден"
$EMU --vfs "$TMP/minimal.zip" --script "$TMP/no_such.emu"
echo "код возврата: $?"

echo "=== ошибка: неизвестный параметр"
$EMU --bogus
echo "код возврата: $?"

echo "=== ошибка: у --script нет значения"
$EMU --vfs "$TMP/minimal.zip" --script
echo "код возврата: $?"

echo "=== для сравнения: оба параметра заданы верно"
$EMU --vfs "$TMP/minimal.zip" --script "$START"

rm -rf "$TMP"
