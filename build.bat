@echo off
pyinstaller -F main.py -i NONE -n autoRunner --distpath ./build/dist --workpath ./build/build
