# Быстрый старт

## Установка

1. Убедитесь что установлен Python 3.10+:
```bash
python --version
```

2. Установите зависимости:
```bash
cd chrome-mcp-server
pip install -r requirements.txt
```

3. Проверьте что Chrome установлен:
```bash
# Windows
"C:\Program Files\Google\Chrome\Application\chrome.exe" --version
```

## Первый запуск

### Вариант 1: Прямой запуск

```bash
python src/server.py
```

### Вариант 2: Интеграция с Claude Desktop

1. Найдите файл конфигурации Claude Desktop:
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

2. Добавьте конфигурацию сервера:

```json
{
  "mcpServers": {
    "chrome-automation": {
      "command": "python",
      "args": ["D:\\Projects\\MCP\\chrome-mcp-server\\src\\server.py"]
    }
  }
}
```

3. Перезапустите Claude Desktop

## Проверка работы

В Claude Desktop попробуйте:

```
Запусти браузер Chrome, открой google.com и сделай скриншот
```

## Примеры команд

### Простой поиск в Google
```
1. Запусти браузер
2. Открой google.com
3. В поле поиска введи "weather today"
4. Нажми кнопку поиска
5. Сделай скриншот
```

### Извлечение данных
```
Открой news.ycombinator.com и получи первые 5 заголовков статей
```

### Заполнение формы
```
1. Открой страницу с формой
2. Заполни поле email значением test@example.com
3. Заполни поле password значением SecurePass123
4. Кликни на кнопку submit
```

## Отладка

Если возникают проблемы:

1. Проверьте логи в консоли
2. Убедитесь что Chrome установлен
3. Проверьте что все зависимости установлены:
```bash
pip list | grep -E "selenium|mcp"
```

4. Попробуйте запустить в headless режиме:
```python
browser_start({"headless": true})
```

## Частые проблемы

### ChromeDriver не найден
Selenium автоматически загружает ChromeDriver. Если возникают проблемы:
```bash
pip install --upgrade selenium
```

### Элемент не найден
Увеличьте timeout в `browser_manager.py`:
```python
self.timeout = 20  # вместо 10
```

### Браузер не закрывается
Вызовите явно:
```
browser_stop
```
