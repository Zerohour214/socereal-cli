@echo off
REM socereal Windows Installer & Builder (with venv and dynamic config.yaml, fixed PyInstaller syntax)

setlocal enabledelayedexpansion
set VENV_DIR=venv

REM Create virtual environment if not present
if exist %VENV_DIR% (
    echo Virtual environment already exists. Skipping creation.
) else (
    python -m venv %VENV_DIR%
    if errorlevel 1 (
        echo Failed to create virtual environment. Make sure Python is installed.
        exit /b 1
    )
)

REM Activate virtual environment and install dependencies
call %VENV_DIR%\Scripts\activate.bat
%VENV_DIR%\Scripts\python.exe -m pip install --upgrade pip
%VENV_DIR%\Scripts\python.exe -m pip install -r requirements.txt
%VENV_DIR%\Scripts\python.exe -m pip install .
%VENV_DIR%\Scripts\python.exe -m pip install pyinstaller

REM Locate config.yaml from rapidocr_onnxruntime
for /f "delims=" %%i in ('%VENV_DIR%\Scripts\python.exe -c "import os, rapidocr_onnxruntime; print(os.path.join(os.path.dirname(rapidocr_onnxruntime.__file__), 'config.yaml'))"') do (
    set "CONFIG_PATH=%%i"
)

if not exist "!CONFIG_PATH!" (
    echo Could not find config.yaml. Make sure rapidocr_onnxruntime is installed.
    exit /b 1
)

REM Escape backslashes
set "CONFIG_PATH_ESC=!CONFIG_PATH:\=\\!"

REM Clean previous build artifacts
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist socereal.spec del socereal.spec
if exist socereal.exe del socereal.exe

REM Print PyInstaller command for debug
echo.
echo Running: %VENV_DIR%\Scripts\pyinstaller.exe --onefile --name socereal --paths=. --collect-all rapidocr_onnxruntime src/cli.py
echo.

REM Build socereal.exe with PyInstaller
%VENV_DIR%\Scripts\pyinstaller.exe --onefile --name socereal --paths=. --collect-all rapidocr_onnxruntime src/cli.py

REM Copy to project root if successful
if exist dist\socereal.exe (
    copy dist\socereal.exe . >nul
    echo socereal.exe created successfully.
) else (
    echo socereal.exe build failed.
    exit /b 1
)

echo.
echo Usage:
echo socereal [images...] -o output.csv

endlocal
