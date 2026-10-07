#!/bin/sh
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
EMU="sh $ROOT/run.sh"
START="$ROOT/examples/stage2_startup.emu"
VFS="$TMP/vfs.zip"

cp "$START" "$TMP/startup.emu"
cd "$TMP" || exit 1

echo "=== относительные пути: --vfs"
echo "exit" | $EMU --vfs vfs.zip

echo "=== относительные пути: --script"
$EMU --script startup.emu

echo "=== оба параметра, обычный порядок"
$EMU --vfs vfs.zip --script startup.emu

echo "=== оба параметра, обратный порядок"
$EMU --script startup.emu --vfs vfs.zip

rm -rf "$TMP"
