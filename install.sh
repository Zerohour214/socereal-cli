#!/usr/bin/env bash
# Installer for socereal on Linux
set -e
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install .

# Try to ensure socereal is on PATH
if command -v socereal >/dev/null 2>&1; then
    echo "socereal installed and on PATH."
else
    if [ -w "$HOME/.local/bin" ]; then
        cp venv/bin/socereal "$HOME/.local/bin/socereal"
        echo "Copied socereal to $HOME/.local/bin."
    else
        echo "Could not place socereal on PATH. Building single binary."
        pip install pyinstaller
        pyinstaller --onefile --name socereal src/cli.py
        echo "Binary created at dist/socereal"
    fi
fi
