@echo off

rem Set current directory as source directory
set "source_dir=%cd%"

rem Set destination directory
set "destination_dir=C:\Users\diluk\AppData\Local\Programs\Python\Python312"

rem Move test.py
if exist "%source_dir%\test.py" (
    move "%source_dir%\test.py" "%destination_dir%\"
    echo test.py moved to %destination_dir%
) else (
    echo test.py not found in %source_dir%
)

rem Move test2.py
if exist "%source_dir%\test2.py" (
    move "%source_dir%\test2.py" "%destination_dir%\"
    echo test2.py moved to %destination_dir%
) else (
    echo test2.py not found in %source_dir%
)

rem Pause to see any messages before closing the window
pause
