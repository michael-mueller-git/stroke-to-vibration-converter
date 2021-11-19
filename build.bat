@echo off
rmdir /Q /S "build" 2>NUL
rmdir /Q /S "dist" 2>NUL
del stroke-to-vibration-converter.spec 2>NUL
pyinstaller --noupx --onefile --noconsole stroke-to-vibration-converter.py

