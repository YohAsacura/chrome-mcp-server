# Структура проекта

```
chrome-mcp-server/
│
├── 📂 src/                      # Исходный код
│   ├── server.py               # MCP сервер (главный файл)
│   ├── browser_manager.py      # Менеджер Chrome браузера
│   └── __init__.py             # Инициализация пакета
│
├── 📂 config/                   # Конфигурация
│   ├── browser_config.json     # Настройки браузера
│   └── claude_desktop_config_example.json  # Пример конфига MCP
│
├── 📂 docs/                     # Документация
│   ├── api.md                  # API Reference (все инструменты)
│   ├── quickstart.md           # Быстрый старт
│   └── examples.md             # Продвинутые примеры
│
├── 📂 examples/                 # Примеры кода
│   └── usage_examples.py       # Python примеры использования
│
├── 📂 scripts/                  # Утилиты
│   ├── install.bat             # Установка зависимостей (Windows)
│   └── start.bat               # Запуск сервера (Windows)
│
├── 📂 tests/                    # Тесты
│   └── test_browser.py         # Unit тесты BrowserManager
│
├── 📄 README.md                 # Главная документация
├── 📄 CHANGELOG.md              # История версий
├── 📄 LICENSE                   # Лицензия MIT
├── 📄 requirements.txt          # Python зависимости
├── 📄 pyproject.toml            # Настройки проекта
├── 📄 .gitignore               # Git ignore
└── 📄 __main__.py              # Entry point для python -m

```

## 📝 Описание компонентов

### Основные файлы

- **`src/server.py`** - MCP сервер, обрабатывает запросы и маршрутизирует вызовы
- **`src/browser_manager.py`** - Класс для управления Chrome через Selenium
- **`README.md`** - Главная документация с быстрым стартом

### Документация

- **`docs/api.md`** - Полное описание всех 13 MCP инструментов
- **`docs/quickstart.md`** - Пошаговая инструкция для новичков
- **`docs/examples.md`** - 10+ продвинутых сценариев использования

### Конфигурация

- **`config/browser_config.json`** - Настройки Chrome (опции, timeout)
- **`config/claude_desktop_config_example.json`** - Пример для Claude Desktop

### Утилиты

- **`scripts/install.bat`** - Автоматическая установка зависимостей
- **`scripts/start.bat`** - Запуск сервера с проверками

## 🎯 Минимальный набор файлов

Для работы сервера необходимы только:

```
src/server.py
src/browser_manager.py
src/__init__.py
requirements.txt
```

Все остальное - документация, примеры и утилиты для удобства.

## 📊 Статистика

- **Всего файлов**: 19
- **Строк кода**: ~700 (src/)
- **Документация**: ~1500 строк
- **Тестов**: 1 файл

---

**Чистая структура без дублирований и лишних файлов** ✅
