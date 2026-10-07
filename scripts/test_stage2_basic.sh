#!/bin/sh
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
EMU="sh $ROOT/run.sh"
START="$ROOT/examples/stage2_startup.emu"
VFS="$TMP/vfs.zip"

echo "=== без параметров"
echo "exit" | $EMU

echo "=== только --vfs (пока только запоминается)"
echo "exit" | $EMU --vfs "$VFS"

echo "=== только --script"
$EMU --script "$START"

echo "=== --vfs и --script вместе"
$EMU --vfs "$VFS" --script "$START"

rm -rf "$TMP"
