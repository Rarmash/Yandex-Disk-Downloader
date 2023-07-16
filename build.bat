@echo off

REM Install requirements
python -m pip install -r requirements.txt pypiwin32 winshell pyinstaller>=5.12 pyinstaller-hooks-contrib==2023.4

REM Build the executable using PyInstaller
python -m PyInstaller --onefile --clean --exclude-module autopep8 --noupx --icon=icon.ico --name=YandexDiskDownloader main.py