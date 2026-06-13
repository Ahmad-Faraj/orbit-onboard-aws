#!/bin/sh
# Install orbit-onboard onto your PATH (~/.local/bin).
set -e
DIR=$(cd "$(dirname "$0")" && pwd)
BIN="$HOME/.local/bin"
mkdir -p "$BIN"
ln -sf "$DIR/orbit-onboard" "$BIN/orbit-onboard"
echo "Installed: $BIN/orbit-onboard"
echo "Ensure ~/.local/bin is on your PATH, then verify Orbit access:"
echo "  glab orbit remote status"
