@echo off
REM Build script for Windows .exe
REM Run this script on a Windows machine to create a standalone Windows executable

echo Building Spectera Editor for Windows...

REM Check if PyInstaller is installed
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo Failed to install PyInstaller. Please install it manually:
        echo   python -m pip install pyinstaller
        exit /b 1
    )
)

REM Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist SpecteraEditor.spec del SpecteraEditor.spec

REM Build the application
echo Building application...
python -m PyInstaller ^
    --name="SpecteraEditor" ^
    --windowed ^
    --onefile ^
    --add-data="README.md;." ^
    --icon=NONE ^
    spectera_editor.py

if errorlevel 1 (
    echo.
    echo Build failed. Please check the error messages above.
    exit /b 1
) else (
    echo.
    echo Build successful!
    echo The executable is located at: dist\SpecteraEditor.exe
    echo.
    echo You can now distribute this .exe file to any Windows machine.
)
