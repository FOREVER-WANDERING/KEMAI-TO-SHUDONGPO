@echo off
chcp 65001 > nul
echo Building SDP Order Sync Tool...

REM Clean environment
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

REM Create empty config and history files if they don't exist
if not exist "config.json" (
    echo {} > config.json
    echo Created empty config.json file
)

if not exist "history.json" (
    echo {"records": []} > history.json
    echo Created empty history.json file
)

REM Build executable with PyInstaller
pyinstaller --clean sdp_sync.spec

echo.
if %ERRORLEVEL% == 0 (
    echo Build successful!
    echo Executable is located in the dist\SDP_Order_Sync_Tool directory
) else (
    echo Build failed, please check error messages
)

pause
