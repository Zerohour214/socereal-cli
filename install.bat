@echo off
REM Installer and builder for socereal on Windows
python -m venv venv
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
pip install .
pip install pyinstaller
pyinstaller --onefile --name socereal src\cli.py > NUL
copy dist\socereal.exe . > NUL
echo socereal.exe created in this directory.

echo.
echo Installation complete. Run the CLI with:
echo socereal [images...] -o output.csv
