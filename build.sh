#!/usr/bin/env bash

set -euo pipefail

cd $(dirname $0)

# Create a virtual environment to run our code
VENV_NAME=".venv"
PYTHON="$VENV_NAME/bin/python"

export PATH=$PATH:$HOME/.local/bin

if ! uv pip install pyinstaller -q; then
  exit 1
fi

uv run pyinstaller --onefile -p src src/__main__.py
tar -czvf dist/archive.tar.gz ./dist/__main__ meta.json
