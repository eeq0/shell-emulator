#!/bin/sh
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
python3 "$ROOT/scripts/make_vfs.py" "$TMP"
EMU="sh $ROOT/run.sh"
export EMU_DIR=docs

for name in stage4_commands stage5_commands; do
    echo "=== examples/$name.emu"
    $EMU --vfs "$TMP/deep.zip" --script "$ROOT/examples/$name.emu"
done

echo "=== deep.zip на диске не изменился после mv и rmdir:"
python3 -m zipfile -l "$TMP/deep.zip"

echo "=== examples/all_commands.emu"
$EMU --vfs "$TMP/deep.zip" --script "$ROOT/examples/all_commands.emu"

rm -rf "$TMP"
