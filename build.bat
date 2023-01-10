@echo off
pyinstaller -F main.py -i NONE -n autoRunner --distpath ./build/dist --workpath ./build/build
set auto_ver=%1
if "%auto_ver%"=="" (
    goto end
) else (
    goto frename
)
:frename
REN .\build\dist\autoRunner.exe autoRunner-%auto_ver%-Win-x86_64.exe
:end
