#!/usr/bin/env bash
# Build and publish to PyPI via uv

set -e

echo "Building..."
uv build

echo "Publishing to PyPI..."
uv publish

echo "Done. Check: https://pypi.org/project/webtomd/"
