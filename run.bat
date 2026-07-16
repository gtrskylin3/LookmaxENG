@echo off
cd /d "%~dp0"
call uv sync
start /B .venv\Scripts\pythonw.exe main.py