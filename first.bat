@echo off

rem
set "source_dir=%cd%"

rem
set "destination_dir=%USERPROFILE%\AppData\Local\Programs\Python\Python312"

rem
if exist "%source_dir%\bg.py" (
    move "%source_dir%\bg.py" "%destination_dir%\"
    echo test.py moved to %destination_dir%
) else (
    echo test.py not found in %source_dir%
)

rem
if exist "%source_dir%\logo.py" (
    move "%source_dir%\logo.py" "%destination_dir%\"
    echo test2.py moved to %destination_dir%
) else (
    echo test2.py not found in %source_dir%
)

rem
pause
