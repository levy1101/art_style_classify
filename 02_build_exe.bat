@echo off
REM ═════════════════════════════════════════════════════════════
REM  Prompt-Hunter - Build EXE Script
REM ═════════════════════════════════════════════════════════════

setlocal enabledelayedexpansion

echo.
echo ═══════════════════════════════════════════════════════════
echo  BUILD EXE - Prompt-Hunter
echo ═══════════════════════════════════════════════════════════
echo.

REM Check Python
echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not installed or not in PATH
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% found
echo.

REM Check virtual environment
if exist "env\Scripts\activate.bat" (
    echo [OK] Virtual environment exists
    call env\Scripts\activate.bat
) else (
    echo [INFO] Virtual environment not found. Creating...
    python -m venv env
    call env\Scripts\activate.bat
    echo [OK] Virtual environment created successfully
)

echo.
echo Installing PyInstaller...
pip install --upgrade pip >nul 2>&1
pip install pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Failed to install PyInstaller
    pause
    exit /b 1
)
echo [OK] PyInstaller installed
echo.

REM Check requirements.txt file
if not exist "requirements.txt" (
    echo [ERROR] requirements.txt file not found
    pause
    exit /b 1
)

echo Installing all packages from requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install packages
    pause
    exit /b 1
)
echo [OK] All packages installed
echo.

REM Check app.py file
if not exist "app.py" (
    echo [ERROR] app.py file not found
    pause
    exit /b 1
)

REM Create build directories
if not exist "build" mkdir build
if not exist "dist" mkdir dist

echo.
echo ═══════════════════════════════════════════════════════════
echo Building EXE file...
echo ═══════════════════════════════════════════════════════════
echo.

REM Build exe with PyInstaller
pyinstaller --onefile ^
    --name="Prompt-Hunter" ^
    --icon=icon.ico ^
    --add-data="templates;templates" ^
    --add-data="static;static" ^
    --add-data="art_style_classifier.h5;." ^
    --add-data=".env;." ^
    --hidden-import=google.genai ^
    --hidden-import=flask ^
    --hidden-import=tensorflow ^
    --hidden-import=keras ^
    --windowed ^
    app.py

if errorlevel 1 (
    echo [ERROR] Build failed
    pause
    exit /b 1
)

echo.
echo [OK] Build completed successfully!
echo.
echo ═══════════════════════════════════════════════════════════
echo Results:
echo   - EXE file location: dist\Prompt-Hunter.exe
echo   - Build folder: build\
echo ═══════════════════════════════════════════════════════════
echo.
echo Notes:
echo   - Place icon file (icon.ico) in current directory
echo   - Copy .env file to same directory as EXE
echo   - Or edit add-data line if you don't have icon
echo.

pause
