@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%"

where py >nul 2>nul
if errorlevel 1 (
    echo Python launcher ^(py^) was not found. Install Python 3.10+ and try again.
    popd
    exit /b 1
)

py -m pip install --upgrade pip
if errorlevel 1 (
    echo Failed to upgrade pip.
    popd
    exit /b 1
)

py -m pip install .
if errorlevel 1 (
    echo Failed to install EasyRemoveBG.
    popd
    exit /b 1
)

py install_context_menu.py
if errorlevel 1 (
    echo Failed to install the Windows context menu entries.
    popd
    exit /b 1
)

echo EasyRemoveBG installed successfully.
popd
pause
