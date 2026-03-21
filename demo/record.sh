#!/usr/bin/env bash
# Record terminal demo for README GIF
# Usage: ./demo/record.sh
# Requires: asciinema, agg (cargo install agg)

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CAST_FILE="$SCRIPT_DIR/demo.cast"
GIF_FILE="$SCRIPT_DIR/demo.gif"

echo "Recording terminal demo..."
echo "Run the following commands in the asciinema session:"
echo "  atlas status"
echo "  atlas connections"
echo ""

# Record with asciinema (auto-play script)
asciinema rec "$CAST_FILE" \
  --cols 100 \
  --rows 35 \
  --command "bash $SCRIPT_DIR/demo-commands.sh" \
  --overwrite

echo ""
echo "Cast file: $CAST_FILE"

# Convert to GIF if agg is available
if command -v agg &>/dev/null; then
  echo "Converting to GIF..."
  agg "$CAST_FILE" "$GIF_FILE" \
    --cols 100 \
    --rows 35 \
    --font-size 14 \
    --speed 1.5 \
    --theme asciinema
  echo "GIF: $GIF_FILE"
else
  echo "Install agg to convert: cargo install agg"
fi
