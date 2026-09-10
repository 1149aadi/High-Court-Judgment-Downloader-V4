@echo off
setlocal
title Build High Court Judgment Downloader V4

cd /d "%~dp0"

echo ============================================================
echo HIGH COURT JUDGMENT DOWNLOADER V4 - EXE BUILD
echo ============================================================
echo.

py --version
if errorlevel 1 (
    echo Python was not found.
    pause
    exit /b 1
)

py -c "import playwright" >nul 2>&1
if errorlevel 1 (
    echo Installing Playwright...
    py -m pip install "playwright>=1.55.0"
    if errorlevel 1 goto :fail
) else (
    echo Playwright already installed.
)

py -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    py -m pip install "pyinstaller>=6.10.0"
    if errorlevel 1 goto :fail
) else (
    echo PyInstaller already installed.
)

echo.
echo Checking V4 syntax...
py -m py_compile High_Court_Judgment_Downloader_v4.py
if errorlevel 1 goto :fail

echo.
echo Building EXE...
py -m PyInstaller ^
    --noconfirm ^
    --clean ^
    --onedir ^
    --console ^
    --name "High_Court_Judgment_Downloader_V4" ^
    "High_Court_Judgment_Downloader_v4.py"

if errorlevel 1 goto :fail

echo.
echo ============================================================
echo BUILD SUCCESSFUL
echo ============================================================
echo.
echo Run:
echo dist\High_Court_Judgment_Downloader_V4\High_Court_Judgment_Downloader_V4.exe
echo.
pause
exit /b 0

:fail
echo.
echo BUILD FAILED.
pause
exit /b 1
