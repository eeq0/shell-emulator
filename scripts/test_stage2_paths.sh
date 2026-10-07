#!/bin/sh
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
python3 "$ROOT/scripts/make_vfs.py" "$TMP"
EMU="sh $ROOT/run.sh"
START="$ROOT/examples/stage2_startup.emu"

cp "$START" "$TMP/startup.emu"
cd "$TMP" || exit 1

echo "=== относительные пути: --vfs"
echo "exit" | $EMU --vfs minimal.zip

echo "=== относительные пути: --script"
$EMU --script startup.emu

echo "=== оба параметра, обычный порядок"
$EMU --vfs files.zip --script startup.emu

echo "=== оба параметра, обратный порядок"
$EMU --script startup.emu --vfs files.zip

rm -rf "$TMP"
