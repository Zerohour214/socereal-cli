@echo off
REM Simple installer for ocrcli on Windows
python -m venv venv
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
pip install .

echo.
echo Installation complete. Run the CLI with:
echo ocrcli [images...] -o output.csv
