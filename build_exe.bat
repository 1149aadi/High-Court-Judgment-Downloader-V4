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

echo Installing/updating required Python packages...
py -m pip install -r requirements.txt
if errorlevel 1 goto :fail

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
