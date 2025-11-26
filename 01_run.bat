@echo off
REM ═════════════════════════════════════════════════════════════
REM  Script chạy dự án Prompt-Hunter
REM ═════════════════════════════════════════════════════════════

setlocal enabledelayedexpansion

echo.
echo ═══════════════════════════════════════════════════════════
echo  PROMPT-HUNTER - Art Style Classifier
echo ═══════════════════════════════════════════════════════════
echo.

REM Kiểm tra file .env
if not exist ".env" (
    echo.
    echo ⚠️  CẢNH BÁO: File .env không tồn tại!
    echo.
    echo Vui lòng tạo file .env trong thư mục hiện tại với nội dung:
    echo.
    echo     GROQ_API_KEY=your_groq_api_key
    echo     GOOGLE_API_KEY=your_google_api_key
    echo.
    echo Sau đó chạy lại file này.
    echo.
    pause
    exit /b 1
)

echo ✓ File .env được tìm thấy
echo.

REM Kiểm tra Python
echo Kiểm tra Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Lỗi: Python chưa được cài đặt hoặc không nằm trong PATH
    echo Vui lòng cài đặt Python 3.8+ từ python.org
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Python %PYTHON_VERSION% được tìm thấy
echo.

REM Kiểm tra virtual environment
echo Kiểm tra virtual environment...
if exist "env\Scripts\activate.bat" (
    echo ✓ Virtual environment tồn tại
    call env\Scripts\activate.bat
) else (
    echo ⚠️  Virtual environment không tồn tại. Tạo mới...
    python -m venv env
    call env\Scripts\activate.bat
    echo ✓ Tạo virtual environment thành công
)

echo.
echo Cài đặt/cập nhật thư viện từ requirements.txt...
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
if errorlevel 1 (
    echo ✗ Lỗi: Không thể cài đặt thư viện
    pause
    exit /b 1
)

echo ✓ Tất cả thư viện đã được cài đặt
echo.

REM Kiểm tra file mô hình
echo Kiểm tra file mô hình AI...
if not exist "art_style_classifier.h5" (
    echo ✗ Lỗi: File art_style_classifier.h5 không tồn tại
    echo Vui lòng tải file mô hình về
    pause
    exit /b 1
)
echo ✓ File mô hình được tìm thấy
echo.

REM Chạy ứng dụng
echo ═══════════════════════════════════════════════════════════
echo Khởi động ứng dụng...
echo ═══════════════════════════════════════════════════════════
echo.
echo Mở trình duyệt và truy cập: http://localhost:5000
echo.
echo Nhấn Ctrl + C để dừng ứng dụng
echo.

python app.py

pause
