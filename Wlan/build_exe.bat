@echo off
chcp 65001 >nul
title Network Learning Lab — Сборка EXE
color 0A

echo.
echo  ╔══════════════════════════════════════════════════╗
echo  ║   Network Learning Lab — Сборка EXE             ║
echo  ║   Предмет: Компьютерные системы                 ║
echo  ╚══════════════════════════════════════════════════╝
echo.

:: ── Шаг 1: установка зависимостей ───────────────────────
echo [1/4] Установка PyInstaller и Pillow...
pip install pyinstaller pillow --quiet --disable-pip-version-check
if %errorlevel% neq 0 (
    echo [ОШИБКА] Не удалось установить зависимости.
    echo         Убедитесь, что Python и pip доступны в PATH.
    pause & exit /b 1
)
echo       OK

:: ── Шаг 2: создание иконки ───────────────────────────────
echo.
echo [2/4] Создание иконки icon.ico...
python create_icon.py
if %errorlevel% neq 0 (
    echo [ПРЕДУПРЕЖДЕНИЕ] Не удалось создать иконку, продолжаем без неё.
    set ICON_OPT=
) else (
    set ICON_OPT=--icon=icon.ico
)

:: ── Шаг 3: сборка EXE ────────────────────────────────────
echo.
echo [3/4] Сборка EXE (это может занять 1-2 минуты)...
echo.

pyinstaller ^
    --onefile ^
    --windowed ^
    --name "NetworkLearningLab" ^
    %ICON_OPT% ^
    --add-data "." ^
    --clean ^
    --noconfirm ^
    network_learning_lab.py

if %errorlevel% neq 0 (
    echo.
    echo [ОШИБКА] Сборка не удалась. Смотрите вывод выше.
    pause & exit /b 1
)

:: ── Шаг 4: результат ─────────────────────────────────────
echo.
echo [4/4] Проверка...
if exist "dist\NetworkLearningLab.exe" (
    echo.
    echo  ╔══════════════════════════════════════════════════╗
    echo  ║   ГОТОВО!                                        ║
    echo  ║                                                  ║
    echo  ║   Файл:  dist\NetworkLearningLab.exe             ║
    echo  ║                                                  ║
    echo  ║   Можно скопировать на любой компьютер          ║
    echo  ║   с Windows и запустить без Python!             ║
    echo  ╚══════════════════════════════════════════════════╝
    echo.
    echo Открыть папку dist?
    choice /c YN /m "Y=Да, N=Нет"
    if %errorlevel%==1 explorer dist
) else (
    echo [ОШИБКА] EXE файл не найден в папке dist\
)

echo.
pause
