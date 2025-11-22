"""Примеры использования Chrome MCP Server."""

# Этот файл содержит примеры того, как можно использовать инструменты сервера

examples = {
    "google_search": {
        "description": "Поиск в Google",
        "steps": [
            {
                "tool": "browser_start",
                "args": {"headless": False}
            },
            {
                "tool": "navigate",
                "args": {"url": "https://www.google.com"}
            },
            {
                "tool": "type_text",
                "args": {
                    "selector": "textarea[name='q']",
                    "text": "MCP protocol",
                    "by": "css"
                }
            },
            {
                "tool": "click_element",
                "args": {
                    "selector": "input[name='btnK']",
                    "by": "css"
                }
            },
            {
                "tool": "screenshot",
                "args": {"filename": "google_results.png"}
            }
        ]
    },
    
    "extract_headlines": {
        "description": "Извлечение заголовков новостей",
        "steps": [
            {
                "tool": "navigate",
                "args": {"url": "https://news.ycombinator.com"}
            },
            {
                "tool": "execute_javascript",
                "args": {
                    "script": """
                    return Array.from(document.querySelectorAll('.titleline > a'))
                        .map(a => a.textContent)
                        .slice(0, 10);
                    """
                }
            }
        ]
    },
    
    "form_filling": {
        "description": "Заполнение формы",
        "steps": [
            {
                "tool": "navigate",
                "args": {"url": "https://example.com/form"}
            },
            {
                "tool": "type_text",
                "args": {
                    "selector": "#name",
                    "text": "John Doe",
                    "by": "id"
                }
            },
            {
                "tool": "type_text",
                "args": {
                    "selector": "#email",
                    "text": "john@example.com",
                    "by": "id"
                }
            },
            {
                "tool": "click_element",
                "args": {
                    "selector": "button[type='submit']",
                    "by": "css"
                }
            }
        ]
    },
    
    "check_element_exists": {
        "description": "Проверка наличия элемента",
        "steps": [
            {
                "tool": "navigate",
                "args": {"url": "https://example.com"}
            },
            {
                "tool": "find_element",
                "args": {
                    "selector": "//h1",
                    "by": "xpath"
                }
            }
        ]
    }
}
