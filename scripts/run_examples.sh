#!/bin/sh
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
python3 "$ROOT/scripts/make_vfs.py" "$TMP"
EMU="sh $ROOT/run.sh"
export EMU_DIR=docs

echo "=== examples/stage4_commands.emu"
$EMU --vfs "$TMP/deep.zip" --script "$ROOT/examples/stage4_commands.emu"

rm -rf "$TMP"
