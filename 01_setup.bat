@echo off
setlocal

REM Kiểm tra thư mục dữ liệu đã chia
if exist "kaggle\working\art_styles\train" if exist "kaggle\working\art_styles\validate" if exist "kaggle\working\art_styles\test" (
    echo Da co du lieu train/validate/test. Tiep tuc setup...
    echo Setup thanh cong. Nhan phim bat ky de thoat.
    pause
    exit /b 0
) else (
    echo Chua co du lieu train/validate/test hoac thieu thu muc.
    echo Vui long xem huong dan tai va giai nen du lieu tai:
    echo https://drive.google.com/file/d/10FkuSbGvZTCURyoKs_JEbBUnFgDFL102/view?usp=sharing
    echo Sau khi tai xong, giai nen vao dung thu muc kaggle\working\art_styles theo dung cau truc.
    pause
    exit /b 1
)
endlocal
