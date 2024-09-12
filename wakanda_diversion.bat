@echo off
rmdir /s /q images
timeout /t 1
call .venv\Scripts\activate
timeout /t 2
:: start copyq
timeout /t 2
python oaxaca2.py
