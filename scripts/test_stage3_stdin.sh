#!/bin/sh
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
python3 "$ROOT/scripts/make_vfs.py" "$TMP"
EMU="sh $ROOT/run.sh"
START="$ROOT/examples/stage3_vfs.emu"

for name in minimal files deep; do
    echo "=== ввод через stdin + VFS: $name.zip"
    printf 'ls\ncd docs\nvfs-init\nls\nfoo\nexit\n' | $EMU --vfs "$TMP/$name.zip"
done

rm -rf "$TMP"
