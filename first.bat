@echo off

rem
set "source_dir=%cd%"

rem
set "destination_dir=%USERPROFILE%\AppData\Local\Programs\Python\Python312"

rem
if exist "%source_dir%\test.py" (
    move "%source_dir%\test.py" "%destination_dir%\"
    echo test.py moved to %destination_dir%
) else (
    echo test.py not found in %source_dir%
)

rem
if exist "%source_dir%\test2.py" (
    move "%source_dir%\test2.py" "%destination_dir%\"
    echo test2.py moved to %destination_dir%
) else (
    echo test2.py not found in %source_dir%
)

rem
pause
