@echo off
cls
call poetry run pyinstaller --onefile --windowed --noconsole --icon ffov\\assets\\favicon.ico --add-data ffov\\assets;ffov\\assets --paths ffov --name ffov ffov\\__main__.py
pause