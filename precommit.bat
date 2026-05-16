@echo off
python -m isort .
if errorlevel 1 exit /b %errorlevel%

python -m black .
if errorlevel 1 exit /b %errorlevel%
