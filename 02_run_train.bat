@echo off
setlocal
REM Kiem tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Khong tim thay Python. Vui long cai Python theo huong dan video sau:
    echo https://www.youtube.com/watch?v=W99c8zVOkkg
    pause
    exit /b 1
)
REM Tao venv neu chua co
if not exist "env" (
    echo Tao moi virtual environment...
    python -m venv env
)
REM Kich hoat venv
call env\Scripts\activate.bat
REM Cai cac thu vien can thiet
if exist "requirements.txt" (
    echo Dang cai cac thu vien tu requirements.txt ...
    pip install -r requirements.txt
) else (
    echo Khong tim thay requirements.txt
)
REM Kiem tra file train_model.py
if not exist "train_model.py" (
    echo Khong tim thay file train_model.py
    pause
    exit /b 1
)
REM Chay train_model.py
python train_model.py
echo Hoan thanh train. Nhan phim bat ky de thoat.
pause
endlocal
