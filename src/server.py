"""MCP Server для управления Chrome браузером."""

import asyncio
import logging
from typing import Any, Optional
from mcp.server import Server
from mcp.types import Tool, TextContent
from pydantic import AnyUrl
import mcp.server.stdio

from browser_manager import BrowserManager

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Создание сервера
server = Server("chrome-automation")
browser = BrowserManager()


# Определение инструментов
TOOLS = [
    Tool(
        name="browser_start",
        description="Запустить Chrome браузер. Можно указать headless режим.",
        inputSchema={
            "type": "object",
            "properties": {
                "headless": {
                    "type": "boolean",
                    "description": "Запустить в headless режиме (без GUI)",
                    "default": False
                }
            }
        }
    ),
    Tool(
        name="browser_stop",
        description="Остановить Chrome браузер и закрыть все окна.",
        inputSchema={
            "type": "object",
            "properties": {}
        }
    ),
    Tool(
        name="navigate",
        description="Открыть URL в браузере. Автоматически запустит браузер если он не запущен.",
        inputSchema={
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL страницы для открытия"
                }
            },
            "required": ["url"]
        }
    ),
    Tool(
        name="click_element",
        description="Кликнуть по элементу на странице. Поддерживает различные типы селекторов.",
        inputSchema={
            "type": "object",
            "properties": {
                "selector": {
                    "type": "string",
                    "description": "Селектор элемента"
                },
                "by": {
                    "type": "string",
                    "description": "Тип селектора: css, xpath, id, name, class, tag",
                    "default": "css",
                    "enum": ["css", "xpath", "id", "name", "class", "tag"]
                }
            },
            "required": ["selector"]
        }
    ),
    Tool(
        name="type_text",
        description="Ввести текст в поле ввода. Можно указать селектор элемента и опционально очистить поле перед вводом.",
        inputSchema={
            "type": "object",
            "properties": {
                "selector": {
                    "type": "string",
                    "description": "Селектор элемента ввода"
                },
                "text": {
                    "type": "string",
                    "description": "Текст для ввода"
                },
                "by": {
                    "type": "string",
                    "description": "Тип селектора: css, xpath, id, name, class, tag",
                    "default": "css",
                    "enum": ["css", "xpath", "id", "name", "class", "tag"]
                },
                "clear_first": {
                    "type": "boolean",
                    "description": "Очистить поле перед вводом",
                    "default": True
                }
            },
            "required": ["selector", "text"]
        }
    ),
    Tool(
        name="find_element",
        description="Найти элемент на странице и получить информацию о нем (текст, тег, видимость).",
        inputSchema={
            "type": "object",
            "properties": {
                "selector": {
                    "type": "string",
                    "description": "Селектор элемента"
                },
                "by": {
                    "type": "string",
                    "description": "Тип селектора: css, xpath, id, name, class, tag",
                    "default": "css",
                    "enum": ["css", "xpath", "id", "name", "class", "tag"]
                }
            },
            "required": ["selector"]
        }
    ),
    Tool(
        name="get_text",
        description="Получить текстовое содержимое элемента на странице.",
        inputSchema={
            "type": "object",
            "properties": {
                "selector": {
                    "type": "string",
                    "description": "Селектор элемента"
                },
                "by": {
                    "type": "string",
                    "description": "Тип селектора: css, xpath, id, name, class, tag",
                    "default": "css",
                    "enum": ["css", "xpath", "id", "name", "class", "tag"]
                }
            },
            "required": ["selector"]
        }
    ),
    Tool(
        name="screenshot",
        description="Сделать скриншот текущей страницы. Можно указать имя файла для сохранения.",
        inputSchema={
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Путь для сохранения скриншота (опционально)"
                }
            }
        }
    ),
    Tool(
        name="execute_javascript",
        description="Выполнить JavaScript код на текущей странице.",
        inputSchema={
            "type": "object",
            "properties": {
                "script": {
                    "type": "string",
                    "description": "JavaScript код для выполнения"
                }
            },
            "required": ["script"]
        }
    ),
    Tool(
        name="get_page_info",
        description="Получить информацию о текущей странице (URL, заголовок, размер).",
        inputSchema={
            "type": "object",
            "properties": {}
        }
    ),
    Tool(
        name="browser_back",
        description="Вернуться на предыдущую страницу в истории браузера.",
        inputSchema={
            "type": "object",
            "properties": {}
        }
    ),
    Tool(
        name="browser_forward",
        description="Перейти на следующую страницу в истории браузера.",
        inputSchema={
            "type": "object",
            "properties": {}
        }
    ),
    Tool(
        name="browser_refresh",
        description="Обновить текущую страницу.",
        inputSchema={
            "type": "object",
            "properties": {}
        }
    ),
    Tool(
        name="get_page_html",
        description="Получить HTML код страницы. Можно получить очищенный от скриптов HTML для анализа структуры.",
        inputSchema={
            "type": "object",
            "properties": {
                "clean": {
                    "type": "boolean",
                    "description": "Очистить от script и style тегов для уменьшения размера",
                    "default": True
                }
            }
        }
    ),
    Tool(
        name="get_all_text",
        description="Получить весь текстовый контент страницы. Быстрая альтернатива скриншоту для анализа содержимого.",
        inputSchema={
            "type": "object",
            "properties": {
                "visible_only": {
                    "type": "boolean",
                    "description": "Получить только видимый текст (без скрытых элементов)",
                    "default": True
                }
            }
        }
    ),
    Tool(
        name="get_elements_info",
        description="Получить информацию о нескольких элементах (текст, атрибуты, видимость). Полезно для анализа списков, таблиц, форм.",
        inputSchema={
            "type": "object",
            "properties": {
                "selector": {
                    "type": "string",
                    "description": "Селектор элементов"
                },
                "by": {
                    "type": "string",
                    "description": "Тип селектора: css, xpath, id, name, class, tag",
                    "default": "css",
                    "enum": ["css", "xpath", "id", "name", "class", "tag"]
                },
                "max_elements": {
                    "type": "integer",
                    "description": "Максимальное количество элементов для возврата",
                    "default": 50
                }
            },
            "required": ["selector"]
        }
    ),
    Tool(
        name="get_page_structure",
        description="Получить структурированную информацию о странице: заголовки, ссылки, формы, изображения, мета-данные. Лучшая альтернатива скриншоту для понимания содержимого.",
        inputSchema={
            "type": "object",
            "properties": {}
        }
    )
]


@server.list_tools()
async def list_tools() -> list[Tool]:
    """Список доступных инструментов."""
    return TOOLS


@server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Обработка вызовов инструментов."""
    
    try:
        if name == "browser_start":
            headless = arguments.get("headless", False)
            browser.headless = headless
            result = browser.start()
            
        elif name == "browser_stop":
            result = browser.stop()
            
        elif name == "navigate":
            url = arguments["url"]
            result = browser.navigate(url)
            
        elif name == "click_element":
            selector = arguments["selector"]
            by = arguments.get("by", "css")
            result = browser.click(selector, by)
            
        elif name == "type_text":
            selector = arguments["selector"]
            text = arguments["text"]
            by = arguments.get("by", "css")
            clear_first = arguments.get("clear_first", True)
            result = browser.type_text(selector, text, by, clear_first)
            
        elif name == "find_element":
            selector = arguments["selector"]
            by = arguments.get("by", "css")
            result = browser.find_element(selector, by)
            
        elif name == "get_text":
            selector = arguments["selector"]
            by = arguments.get("by", "css")
            result = browser.get_text(selector, by)
            
        elif name == "screenshot":
            filename = arguments.get("filename")
            result = browser.screenshot(filename)
            
        elif name == "execute_javascript":
            script = arguments["script"]
            result = browser.execute_script(script)
            
        elif name == "get_page_info":
            result = browser.get_page_info()
            
        elif name == "browser_back":
            result = browser.back()
            
        elif name == "browser_forward":
            result = browser.forward()
            
        elif name == "browser_refresh":
            result = browser.refresh()
            
        elif name == "get_page_html":
            clean = arguments.get("clean", True)
            result = browser.get_page_html(clean)
            
        elif name == "get_all_text":
            visible_only = arguments.get("visible_only", True)
            result = browser.get_all_text(visible_only)
            
        elif name == "get_elements_info":
            selector = arguments["selector"]
            by = arguments.get("by", "css")
            max_elements = arguments.get("max_elements", 50)
            result = browser.get_elements_info(selector, by, max_elements)
            
        elif name == "get_page_structure":
            result = browser.get_page_structure()
            
        else:
            result = {
                "success": False,
                "error": f"Неизвестный инструмент: {name}"
            }
        
        # Форматирование результата
        return [TextContent(
            type="text",
            text=str(result)
        )]
        
    except Exception as e:
        logger.error(f"Ошибка при выполнении {name}: {e}")
        return [TextContent(
            type="text",
            text=str({
                "success": False,
                "error": str(e)
            })
        )]


async def main():
    """Запуск MCP сервера."""
    logger.info("Запуск Chrome MCP Server...")
    
    try:
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )
    finally:
        # Остановка браузера при завершении
        browser.stop()
        logger.info("Chrome MCP Server остановлен")


if __name__ == "__main__":
    asyncio.run(main())
