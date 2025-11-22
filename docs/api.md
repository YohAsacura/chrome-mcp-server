# API Reference

Полное описание всех доступных инструментов Chrome MCP Server.

## Управление браузером

### browser_start

Запускает Chrome браузер.

**Параметры:**
- `headless` (boolean, опционально) - Запуск в headless режиме. По умолчанию: `false`

**Пример:**
```json
{
  "tool": "browser_start",
  "arguments": {
    "headless": false
  }
}
```

**Ответ:**
```json
{
  "success": true,
  "message": "Chrome браузер успешно запущен",
  "headless": false
}
```

---

### browser_stop

Останавливает браузер и закрывает все окна.

**Параметры:** нет

**Пример:**
```json
{
  "tool": "browser_stop",
  "arguments": {}
}
```

**Ответ:**
```json
{
  "success": true,
  "message": "Браузер успешно остановлен"
}
```

---

## Навигация

### navigate

Открывает указанный URL в браузере.

**Параметры:**
- `url` (string, обязательно) - URL страницы для открытия

**Пример:**
```json
{
  "tool": "navigate",
  "arguments": {
    "url": "https://www.google.com"
  }
}
```

**Ответ:**
```json
{
  "success": true,
  "url": "https://www.google.com/",
  "title": "Google"
}
```

---

### browser_back

Возвращается на предыдущую страницу в истории браузера.

**Параметры:** нет

---

### browser_forward

Переходит на следующую страницу в истории браузера.

**Параметры:** нет

---

### browser_refresh

Обновляет текущую страницу.

**Параметры:** нет

---

## Взаимодействие с элементами

### click_element

Кликает по элементу на странице.

**Параметры:**
- `selector` (string, обязательно) - Селектор элемента
- `by` (string, опционально) - Тип селектора. Допустимые значения: `css`, `xpath`, `id`, `name`, `class`, `tag`. По умолчанию: `css`

**Примеры:**

CSS селектор:
```json
{
  "tool": "click_element",
  "arguments": {
    "selector": "button.submit",
    "by": "css"
  }
}
```

XPath:
```json
{
  "tool": "click_element",
  "arguments": {
    "selector": "//button[text()='Submit']",
    "by": "xpath"
  }
}
```

По ID:
```json
{
  "tool": "click_element",
  "arguments": {
    "selector": "submit-btn",
    "by": "id"
  }
}
```

**Ответ:**
```json
{
  "success": true,
  "message": "Выполнен клик по элементу: button.submit"
}
```

---

### type_text

Вводит текст в поле ввода.

**Параметры:**
- `selector` (string, обязательно) - Селектор элемента
- `text` (string, обязательно) - Текст для ввода
- `by` (string, опционально) - Тип селектора. По умолчанию: `css`
- `clear_first` (boolean, опционально) - Очистить поле перед вводом. По умолчанию: `true`

**Пример:**
```json
{
  "tool": "type_text",
  "arguments": {
    "selector": "input[name='search']",
    "text": "Hello World",
    "by": "css",
    "clear_first": true
  }
}
```

**Ответ:**
```json
{
  "success": true,
  "message": "Текст введен в элемент: input[name='search']"
}
```

---

### find_element

Ищет элемент на странице и возвращает информацию о нем.

**Параметры:**
- `selector` (string, обязательно) - Селектор элемента
- `by` (string, опционально) - Тип селектора. По умолчанию: `css`

**Пример:**
```json
{
  "tool": "find_element",
  "arguments": {
    "selector": "h1",
    "by": "tag"
  }
}
```

**Ответ (элемент найден):**
```json
{
  "success": true,
  "found": true,
  "text": "Welcome",
  "tag": "h1",
  "visible": true
}
```

**Ответ (элемент не найден):**
```json
{
  "success": true,
  "found": false,
  "message": "Элемент не найден: h1"
}
```

---

### get_text

Получает текстовое содержимое элемента.

**Параметры:**
- `selector` (string, обязательно) - Селектор элемента
- `by` (string, опционально) - Тип селектора. По умолчанию: `css`

**Пример:**
```json
{
  "tool": "get_text",
  "arguments": {
    "selector": ".title",
    "by": "css"
  }
}
```

**Ответ:**
```json
{
  "success": true,
  "text": "Page Title"
}
```

---

## Дополнительные возможности

### screenshot

Создает скриншот текущей страницы.

**Параметры:**
- `filename` (string, опционально) - Путь для сохранения скриншота

**Пример без сохранения:**
```json
{
  "tool": "screenshot",
  "arguments": {}
}
```

**Пример с сохранением:**
```json
{
  "tool": "screenshot",
  "arguments": {
    "filename": "screenshot.png"
  }
}
```

**Ответ:**
```json
{
  "success": true,
  "screenshot_base64": "iVBORw0KGgoAAAANSUhEUgAA...",
  "url": "https://www.example.com",
  "filename": "screenshot.png"
}
```

---

### execute_javascript

Выполняет JavaScript код на текущей странице.

**Параметры:**
- `script` (string, обязательно) - JavaScript код для выполнения

**Примеры:**

Получить заголовок:
```json
{
  "tool": "execute_javascript",
  "arguments": {
    "script": "return document.title;"
  }
}
```

Получить все ссылки:
```json
{
  "tool": "execute_javascript",
  "arguments": {
    "script": "return Array.from(document.querySelectorAll('a')).map(a => a.href);"
  }
}
```

Прокрутка вниз:
```json
{
  "tool": "execute_javascript",
  "arguments": {
    "script": "window.scrollTo(0, document.body.scrollHeight);"
  }
}
```

**Ответ:**
```json
{
  "success": true,
  "result": "Example Domain"
}
```

---

### get_page_info

Получает информацию о текущей странице.

**Параметры:** нет

**Пример:**
```json
{
  "tool": "get_page_info",
  "arguments": {}
}
```

**Ответ:**
```json
{
  "success": true,
  "url": "https://www.example.com",
  "title": "Example Domain",
  "page_source_length": 1256
}
```

---

## Типы селекторов

### CSS Selector (`by: "css"`)

Примеры:
- `.class` - по классу
- `#id` - по ID
- `tag` - по тегу
- `[attribute="value"]` - по атрибуту
- `parent > child` - прямой потомок
- `element:nth-child(n)` - n-й элемент

### XPath (`by: "xpath"`)

Примеры:
- `//tag` - все элементы tag
- `//tag[@id="value"]` - по атрибуту
- `//tag[text()="text"]` - по тексту
- `//tag[contains(@class, "value")]` - частичное совпадение
- `(//tag)[1]` - первый элемент

### ID (`by: "id"`)

Пример: `"submit-button"` (без `#`)

### Name (`by: "name"`)

Пример: `"email"` (значение атрибута name)

### Class (`by: "class"`)

Пример: `"btn-primary"` (без `.`)

### Tag (`by: "tag"`)

Пример: `"button"`, `"input"`, `"div"`

---

## Обработка ошибок

Все инструменты возвращают объект с полем `success`:

**Успешное выполнение:**
```json
{
  "success": true,
  ...
}
```

**Ошибка:**
```json
{
  "success": false,
  "error": "Описание ошибки"
}
```

### Типичные ошибки

- `"Браузер не запущен"` - нужно вызвать `browser_start`
- `"Элемент не найден"` - элемент отсутствует или селектор неверный
- `"TimeoutException"` - элемент не появился в течение timeout (10 сек)
- `"NoSuchElementException"` - элемент не существует на странице

---

## Рекомендации

### Ожидание загрузки

После навигации дождитесь загрузки страницы:

```json
{
  "tool": "execute_javascript",
  "arguments": {
    "script": "return document.readyState === 'complete';"
  }
}
```

### Проверка существования элемента

Используйте `find_element` перед взаимодействием:

```json
{
  "tool": "find_element",
  "arguments": {
    "selector": "button.submit"
  }
}
```

### Headless режим для автоматизации

Для фоновых задач используйте headless:

```json
{
  "tool": "browser_start",
  "arguments": {
    "headless": true
  }
}
```

### Timeout

По умолчанию timeout для поиска элементов - 10 секунд. Для изменения отредактируйте `src/browser_manager.py`:

```python
self.timeout = 20  # увеличить до 20 секунд
```

---

## Новые инструменты для анализа страниц

> ⭐ **Рекомендуется использовать вместо скриншотов** - быстрее, дешевле, больше информации!

### get_page_structure

Получает структурированную информацию о странице: заголовки, ссылки, формы, изображения, мета-данные.

**Параметры:** нет

**Пример:**
```json
{
  "tool": "get_page_structure",
  "arguments": {}
}
```

**Ответ:**
```json
{
  "success": true,
  "structure": {
    "url": "https://example.com",
    "title": "Example Domain",
    "headings": {
      "h1": ["Example Domain"],
      "h2": ["More information...", "Contact"],
      "h3": []
    },
    "links": [
      {
        "text": "More information",
        "href": "https://example.com/info",
        "internal": true
      }
    ],
    "images": [
      {
        "src": "https://example.com/logo.png",
        "alt": "Logo"
      }
    ],
    "forms": [
      {
        "action": "/search",
        "method": "get",
        "inputs": [
          {
            "type": "text",
            "name": "q",
            "id": "search",
            "placeholder": "Search..."
          }
        ]
      }
    ],
    "meta": {
      "description": "Example Domain for testing",
      "keywords": "example, domain, test",
      "viewport": "width=device-width, initial-scale=1"
    }
  }
}
```

---

### get_all_text

Получает весь текстовый контент страницы. **Быстрая альтернатива скриншоту.**

**Параметры:**
- `visible_only` (boolean, опционально) - Получить только видимый текст. По умолчанию: `true`

**Пример:**
```json
{
  "tool": "get_all_text",
  "arguments": {
    "visible_only": true
  }
}
```

**Ответ:**
```json
{
  "success": true,
  "text": "Example Domain\nThis domain is for use in illustrative examples...",
  "length": 523,
  "url": "https://example.com"
}
```

---

### get_page_html

Получает HTML код страницы.

**Параметры:**
- `clean` (boolean, опционально) - Очистить от script и style тегов. По умолчанию: `true`

**Пример:**
```json
{
  "tool": "get_page_html",
  "arguments": {
    "clean": true
  }
}
```

**Ответ:**
```json
{
  "success": true,
  "html": "<!DOCTYPE html><html><head>...</head><body>...</body></html>",
  "length": 1256,
  "url": "https://example.com",
  "title": "Example Domain"
}
```

---

### get_elements_info

Получает информацию о нескольких элементах. Полезно для анализа списков, таблиц, карточек товаров.

**Параметры:**
- `selector` (string, обязательно) - Селектор элементов
- `by` (string, опционально) - Тип селектора. По умолчанию: `css`
- `max_elements` (integer, опционально) - Максимум элементов. По умолчанию: `50`

**Пример:**
```json
{
  "tool": "get_elements_info",
  "arguments": {
    "selector": ".product-card",
    "by": "css",
    "max_elements": 10
  }
}
```

**Ответ:**
```json
{
  "success": true,
  "count": 10,
  "selector": ".product-card",
  "elements": [
    {
      "index": 0,
      "tag": "div",
      "text": "iPhone 15 Pro\n$999",
      "visible": true,
      "enabled": true,
      "attributes": {
        "id": "product-1",
        "class": "product-card featured",
        "href": null,
        "src": null,
        "type": null,
        "value": null
      }
    },
    {
      "index": 1,
      "tag": "div",
      "text": "Samsung Galaxy S24\n$899",
      "visible": true,
      "enabled": true,
      "attributes": {
        "id": "product-2",
        "class": "product-card",
        "href": null,
        "src": null,
        "type": null,
        "value": null
      }
    }
  ]
}
```

---

## Сравнение: скриншот vs текстовые данные

| Критерий | Screenshot | get_page_structure / get_all_text |
|----------|-----------|----------------------------------|
| **Скорость** | Медленно (~500ms) | Быстро (~50ms) |
| **Размер данных** | Большой (base64) | Компактный (JSON/текст) |
| **Анализ AI** | Требует vision модель | Работает с обычными моделями |
| **Стоимость** | Выше (vision API) | Ниже (text API) |
| **Точность данных** | Визуальная | Структурированная |
| **Use case** | Верстка, дизайн | Контент, данные, формы |

**Рекомендация:** Используйте `get_page_structure` или `get_all_text` для анализа контента. Скриншоты оставьте для визуальной проверки.

---

**Версия API**: 0.2.0  
**Дата обновления**: 2024-11-22
