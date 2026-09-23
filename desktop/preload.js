const { contextBridge } = require('electron');

// Флаг для игровой страницы: внутри Electron скрываем веб-баннер «Скачать»
contextBridge.exposeInMainWorld('busikDesktop', true);
