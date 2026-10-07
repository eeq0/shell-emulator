#!/bin/sh
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
python3 "$ROOT/scripts/make_vfs.py" "$TMP"
EMU="sh $ROOT/run.sh"
START="$ROOT/examples/stage3_vfs.emu"

for name in minimal files deep; do
    echo "=== скрипт + VFS: $name.zip"
    $EMU --vfs "$TMP/$name.zip" --script "$START"
done

rm -rf "$TMP"
