"""Базовые тесты для Chrome MCP Server."""

import pytest
import asyncio
from src.browser_manager import BrowserManager


class TestBrowserManager:
    """Тесты для BrowserManager."""
    
    @pytest.fixture
    def browser(self):
        """Фикстура браузера."""
        browser = BrowserManager(headless=True)
        yield browser
        browser.stop()
    
    def test_browser_start_stop(self, browser):
        """Тест запуска и остановки браузера."""
        result = browser.start()
        assert result["success"] is True
        
        result = browser.stop()
        assert result["success"] is True
    
    def test_navigate(self, browser):
        """Тест навигации."""
        browser.start()
        result = browser.navigate("https://www.example.com")
        assert result["success"] is True
        assert "example.com" in result["url"].lower()
    
    def test_get_page_info(self, browser):
        """Тест получения информации о странице."""
        browser.start()
        browser.navigate("https://www.example.com")
        
        result = browser.get_page_info()
        assert result["success"] is True
        assert "url" in result
        assert "title" in result
    
    def test_find_element(self, browser):
        """Тест поиска элемента."""
        browser.start()
        browser.navigate("https://www.example.com")
        
        result = browser.find_element("h1", by="tag")
        assert result["success"] is True
    
    def test_screenshot(self, browser):
        """Тест создания скриншота."""
        browser.start()
        browser.navigate("https://www.example.com")
        
        result = browser.screenshot()
        assert result["success"] is True
        assert "screenshot_base64" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
