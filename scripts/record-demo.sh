#!/usr/bin/env bash
# Record terminal demo GIFs using vhs (https://github.com/charmbracelet/vhs)
# Install: brew install vhs

set -e

echo "Recording core demo..."
vhs demo.tape -o ../docs/demo.gif

echo "Recording AI demo..."
vhs demo-ai.tape -o ../docs/demo-ai.gif

echo "Done. GIFs saved to docs/"
