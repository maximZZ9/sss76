#!/usr/bin/env python3
"""Генератор автономного .bat-установщика Flappy Бусик.

Читает desktop/game/index.html, кодирует в base64 и собирает
одиночный бат-файл, который:
  * распаковывает игру в %LOCALAPPDATA%\\FlappyBusik (certutil -decode);
  * создаёт ярлык на рабочем столе и в меню «Пуск» (PowerShell);
  * предлагает сразу запустить игру.

Запуск:  python3 desktop/tools/make_bat.py
Результат: desktop/install-flappy-busik.bat
"""
import base64
import pathlib

TOOLS = pathlib.Path(__file__).resolve().parent
DESKTOP = TOOLS.parent
GAME = DESKTOP / "game" / "index.html"
OUT = DESKTOP / "install-flappy-busik.bat"

CHUNK = 500  # символов base64 на строку (лимит строки cmd — 8191)

b64 = base64.b64encode(GAME.read_bytes()).decode("ascii")
chunks = [b64[i:i + CHUNK] for i in range(0, len(b64), CHUNK)]

lines = [
    "@echo off",
    "setlocal EnableDelayedExpansion",
    "chcp 65001 >nul",
    "title Установка Flappy Бусик",
    "color 0A",
    "echo.",
    "echo   ============================================",
    "echo      FLAPPY БУСИК — ТЦК SIMULATOR",
    "echo      Установка игры (автономный установщик)",
    "echo   ============================================",
    "echo.",
    'set "DEST=%LOCALAPPDATA%\\FlappyBusik"',
    'set "HTML=%DEST%\\FlappyBusik.html"',
    'set "B64F=%TEMP%\\flappy_busik_b64.txt"',
    "echo Создаю папку: %DEST%",
    'if not exist "%DEST%" mkdir "%DEST%"',
    'if exist "%HTML%" del "%HTML%" >nul 2>&1',
    'if exist "%B64F%" del "%B64F%" >nul 2>&1',
]
lines += ['>>"%B64F%" echo ' + c for c in chunks]
lines += [
    "echo Распаковываю игру...",
    'certutil -f -decode "%B64F%" "%HTML%" >nul 2>&1',
    "if errorlevel 1 (",
    "  echo ОШИБКА распаковки. Сообщите разработчику.",
    "  pause",
    "  exit /b 1",
    ")",
    'del "%B64F%" >nul 2>&1',
    "echo Создаю ярлык на рабочем столе...",
    "powershell -NoProfile -Command \"$s=(New-Object -ComObject WScript.Shell).CreateShortcut([Environment]::GetFolderPath('Desktop')+'\\Flappy Busik.lnk');$s.TargetPath='%HTML%';$s.Save()\" >nul 2>&1",
    "echo Создаю ярлык в меню «Пуск»...",
    "powershell -NoProfile -Command \"$sm=[Environment]::GetFolderPath('StartMenu')+'\\Programs';$s=(New-Object -ComObject WScript.Shell).CreateShortcut($sm+'\\Flappy Busik.lnk');$s.TargetPath='%HTML%';$s.Save()\" >nul 2>&1",
    "echo.",
    "echo   ============================================",
    'echo   Готово! Ярлык "Flappy Busik" на рабочем столе.',
    "echo   Игра работает полностью офлайн.",
    "echo   ============================================",
    "echo.",
    'choice /c YN /n /m "Запустить игру сейчас? [Y - да, N - нет] "',
    "if errorlevel 2 goto end",
    'start "" "%HTML%"',
    ":end",
    "endlocal",
]

OUT.write_text("\r\n".join(lines) + "\r\n", encoding="utf-8", newline="")
print(f"OK: {OUT} ({OUT.stat().st_size} байт, {len(chunks)} chunk-строк)")
