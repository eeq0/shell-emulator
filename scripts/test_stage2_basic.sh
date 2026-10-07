#!/bin/sh
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
python3 "$ROOT/scripts/make_vfs.py" "$TMP"
EMU="sh $ROOT/run.sh"
START="$ROOT/examples/stage2_startup.emu"

echo "=== без параметров"
echo "exit" | $EMU

echo "=== только --vfs"
echo "exit" | $EMU --vfs "$TMP/minimal.zip"

echo "=== только --script"
$EMU --script "$START"

echo "=== --vfs и --script вместе"
$EMU --vfs "$TMP/files.zip" --script "$START"

rm -rf "$TMP"
