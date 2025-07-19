@echo off
REM Installer and builder for socereal on Windows

REM Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist socereal.spec del socereal.spec
if exist socereal.exe del socereal.exe

REM Setup virtual environment and install dependencies
python -m venv venv
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
pip install .
pip install pyinstaller

REM Build the EXE
pyinstaller --onefile --name socereal --paths=. src/cli.py > NUL

REM Copy EXE to root
copy dist\socereal.exe . > NUL

echo socereal.exe created in this directory.

echo.
echo Installation complete. Run the CLI with:
echo socereal [images...] -o output.csv
