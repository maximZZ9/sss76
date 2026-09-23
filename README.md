# sss76

## 🚌 Flappy Бусик — ТЦК Simulator

Flappy Bird, где вместо птички — летающий бусик ТЦК. Уворачивайся от столбов, собирай повістки.

### Веб-версия (в браузере)
Открой `index.html` — или сыграй в живом превью (порт 8000).

```bash
python3 -m http.server 8000
# → http://localhost:8000
```

### 📦 Версии для Windows

| Вариант | Что это | Где взять |
|---|---|---|
| **FlappyBusik-Setup-1.0.0.exe** | Полноценный установщик (NSIS): ярлыки, выбор папки, удаление через Панель управления | Артефакт `FlappyBusik-Windows` на странице [Actions-запуска](https://github.com/maximZZ9/sss76/actions/workflows/build-installer.yml) |
| **FlappyBusik-Portable-1.0.0.exe** | Portable, без установки | Там же |
| **install-flappy-busik.bat** | Лёгкий автономный установщик (один файл, без Electron, игра в браузере) | [Скачать из репозитория](desktop/install-flappy-busik.bat) |

CI собирает exe на каждом пуше (`.github/workflows/build-installer.yml`).

### 🎮 Управление
- **Тап / клик / пробел / ↑ / W** — газ (флап)
- **P** — пауза, **M** — звук

### Структура
```
index.html                      — веб-версия игры (один файл)
desktop/main.js                 — Electron: главное окно
desktop/preload.js              — preload (флаг busikDesktop)
desktop/game/index.html         — копия игры для упаковки
desktop/buildres/               — иконки (icon.ico)
desktop/tools/make_bat.py       — генератор автономного .bat-установщика
desktop/install-flappy-busik.bat— готовый .bat-установщик (игра внутри в base64)
.github/workflows/build-installer.yml — CI: сборка NSIS + portable
```
