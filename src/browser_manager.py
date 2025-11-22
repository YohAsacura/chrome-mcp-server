"""Управление браузером Chrome через Selenium."""

import os
import logging
from typing import Optional, List, Dict, Any
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import base64

logger = logging.getLogger(__name__)


class BrowserManager:
    """Менеджер для управления Chrome браузером."""
    
    def __init__(self, headless: bool = False):
        """
        Инициализация менеджера браузера.
        
        Args:
            headless: Запускать браузер в headless режиме
        """
        self.driver: Optional[webdriver.Chrome] = None
        self.headless = headless
        self.timeout = 10
        
    def start(self) -> Dict[str, Any]:
        """Запуск браузера Chrome."""
        try:
            if self.driver:
                return {
                    "success": True,
                    "message": "Браузер уже запущен"
                }
            
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument("--headless")
            
            # Дополнительные опции для стабильной работы
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.maximize_window()
            
            logger.info("Chrome браузер успешно запущен")
            return {
                "success": True,
                "message": "Chrome браузер успешно запущен",
                "headless": self.headless
            }
            
        except Exception as e:
            logger.error(f"Ошибка при запуске браузера: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def stop(self) -> Dict[str, Any]:
        """Остановка браузера."""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
                logger.info("Браузер остановлен")
                return {
                    "success": True,
                    "message": "Браузер успешно остановлен"
                }
            return {
                "success": True,
                "message": "Браузер не был запущен"
            }
        except Exception as e:
            logger.error(f"Ошибка при остановке браузера: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def navigate(self, url: str) -> Dict[str, Any]:
        """
        Переход по URL.
        
        Args:
            url: Адрес страницы
        """
        try:
            if not self.driver:
                self.start()
            
            self.driver.get(url)
            logger.info(f"Переход на страницу: {url}")
            
            return {
                "success": True,
                "url": self.driver.current_url,
                "title": self.driver.title
            }
        except Exception as e:
            logger.error(f"Ошибка при переходе на {url}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_page_info(self) -> Dict[str, Any]:
        """Получение информации о текущей странице."""
        try:
            if not self.driver:
                return {
                    "success": False,
                    "error": "Браузер не запущен"
                }
            
            return {
                "success": True,
                "url": self.driver.current_url,
                "title": self.driver.title,
                "page_source_length": len(self.driver.page_source)
            }
        except Exception as e:
            logger.error(f"Ошибка при получении информации о странице: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def find_element(
        self, 
        selector: str, 
        by: str = "css"
    ) -> Dict[str, Any]:
        """
        Поиск элемента на странице.
        
        Args:
            selector: Селектор элемента
            by: Тип селектора (css, xpath, id, name, class, tag)
        """
        try:
            if not self.driver:
                return {
                    "success": False,
                    "error": "Браузер не запущен"
                }
            
            by_mapping = {
                "css": By.CSS_SELECTOR,
                "xpath": By.XPATH,
                "id": By.ID,
                "name": By.NAME,
                "class": By.CLASS_NAME,
                "tag": By.TAG_NAME
            }
            
            by_type = by_mapping.get(by.lower(), By.CSS_SELECTOR)
            
            wait = WebDriverWait(self.driver, self.timeout)
            element = wait.until(
                EC.presence_of_element_located((by_type, selector))
            )
            
            return {
                "success": True,
                "found": True,
                "text": element.text,
                "tag": element.tag_name,
                "visible": element.is_displayed()
            }
            
        except TimeoutException:
            return {
                "success": True,
                "found": False,
                "message": f"Элемент не найден: {selector}"
            }
        except Exception as e:
            logger.error(f"Ошибка при поиске элемента {selector}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def click(
        self, 
        selector: str, 
        by: str = "css"
    ) -> Dict[str, Any]:
        """
        Клик по элементу.
        
        Args:
            selector: Селектор элемента
            by: Тип селектора
        """
        try:
            if not self.driver:
                return {
                    "success": False,
                    "error": "Браузер не запущен"
                }
            
            by_mapping = {
                "css": By.CSS_SELECTOR,
                "xpath": By.XPATH,
                "id": By.ID,
                "name": By.NAME,
                "class": By.CLASS_NAME,
                "tag": By.TAG_NAME
            }
            
            by_type = by_mapping.get(by.lower(), By.CSS_SELECTOR)
            
            wait = WebDriverWait(self.driver, self.timeout)
            element = wait.until(
                EC.element_to_be_clickable((by_type, selector))
            )
            element.click()
            
            logger.info(f"Клик по элементу: {selector}")
            return {
                "success": True,
                "message": f"Выполнен клик по элементу: {selector}"
            }
            
        except Exception as e:
            logger.error(f"Ошибка при клике по {selector}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def type_text(
        self, 
        selector: str, 
        text: str, 
        by: str = "css",
        clear_first: bool = True
    ) -> Dict[str, Any]:
        """
        Ввод текста в элемент.
        
        Args:
            selector: Селектор элемента
            text: Текст для ввода
            by: Тип селектора
            clear_first: Очистить поле перед вводом
        """
        try:
            if not self.driver:
                return {
                    "success": False,
                    "error": "Браузер не запущен"
                }
            
            by_mapping = {
                "css": By.CSS_SELECTOR,
                "xpath": By.XPATH,
                "id": By.ID,
                "name": By.NAME,
                "class": By.CLASS_NAME,
                "tag": By.TAG_NAME
            }
            
            by_type = by_mapping.get(by.lower(), By.CSS_SELECTOR)
            
            wait = WebDriverWait(self.driver, self.timeout)
            element = wait.until(
                EC.presence_of_element_located((by_type, selector))
            )
            
            if clear_first:
                element.clear()
            
            element.send_keys(text)
            
            logger.info(f"Введен текст в элемент: {selector}")
            return {
                "success": True,
                "message": f"Текст введен в элемент: {selector}"
            }
            
        except Exception as e:
            logger.error(f"Ошибка при вводе текста в {selector}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def screenshot(self, filename: Optional[str] = None) -> Dict[str, Any]:
        """
        Создание скриншота страницы.
        
        Args:
            filename: Имя файла для сохранения (опционально)
        """
        try:
            if not self.driver:
                return {
                    "success": False,
                    "error": "Браузер не запущен"
                }
            
            screenshot_base64 = self.driver.get_screenshot_as_base64()
            
            result = {
                "success": True,
                "screenshot_base64": screenshot_base64,
                "url": self.driver.current_url
            }
            
            if filename:
                self.driver.save_screenshot(filename)
                result["filename"] = filename
                logger.info(f"Скриншот сохранен: {filename}")
            
            return result
            
        except Exception as e:
            logger.error(f"Ошибка при создании скриншота: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def execute_script(self, script: str) -> Dict[str, Any]:
        """
        Выполнение JavaScript на странице.
        
        Args:
            script: JavaScript код
        """
        try:
            if not self.driver:
                return {
                    "success": False,
                    "error": "Браузер не запущен"
                }
            
            result = self.driver.execute_script(script)
            
            logger.info("JavaScript выполнен")
            return {
                "success": True,
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Ошибка при выполнении JavaScript: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_text(self, selector: str, by: str = "css") -> Dict[str, Any]:
        """
        Получение текста элемента.
        
        Args:
            selector: Селектор элемента
            by: Тип селектора
        """
        try:
            if not self.driver:
                return {
                    "success": False,
                    "error": "Браузер не запущен"
                }
            
            by_mapping = {
                "css": By.CSS_SELECTOR,
                "xpath": By.XPATH,
                "id": By.ID,
                "name": By.NAME,
                "class": By.CLASS_NAME,
                "tag": By.TAG_NAME
            }
            
            by_type = by_mapping.get(by.lower(), By.CSS_SELECTOR)
            
            wait = WebDriverWait(self.driver, self.timeout)
            element = wait.until(
                EC.presence_of_element_located((by_type, selector))
            )
            
            return {
                "success": True,
                "text": element.text
            }
            
        except Exception as e:
            logger.error(f"Ошибка при получении текста из {selector}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def back(self) -> Dict[str, Any]:
        """Возврат на предыдущую страницу."""
        try:
            if not self.driver:
                return {
                    "success": False,
                    "error": "Браузер не запущен"
                }
            
            self.driver.back()
            return {
                "success": True,
                "url": self.driver.current_url
            }
        except Exception as e:
            logger.error(f"Ошибка при возврате назад: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def forward(self) -> Dict[str, Any]:
        """Переход на следующую страницу."""
        try:
            if not self.driver:
                return {
                    "success": False,
                    "error": "Браузер не запущен"
                }
            
            self.driver.forward()
            return {
                "success": True,
                "url": self.driver.current_url
            }
        except Exception as e:
            logger.error(f"Ошибка при переходе вперед: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def refresh(self) -> Dict[str, Any]:
        """Обновление страницы."""
        try:
            if not self.driver:
                return {
                    "success": False,
                    "error": "Браузер не запущен"
                }
            
            self.driver.refresh()
            return {
                "success": True,
                "url": self.driver.current_url
            }
        except Exception as e:
            logger.error(f"Ошибка при обновлении страницы: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_page_html(self, clean: bool = True) -> Dict[str, Any]:
        """
        Получение HTML кода страницы.
        
        Args:
            clean: Очистить скрипты и стили для уменьшения размера
        """
        try:
            if not self.driver:
                return {
                    "success": False,
                    "error": "Браузер не запущен"
                }
            
            if clean:
                # Получаем HTML без script и style тегов для меньшего размера
                html = self.driver.execute_script("""
                    const clone = document.documentElement.cloneNode(true);
                    clone.querySelectorAll('script, style, noscript').forEach(el => el.remove());
                    return clone.outerHTML;
                """)
            else:
                html = self.driver.page_source
            
            return {
                "success": True,
                "html": html,
                "length": len(html),
                "url": self.driver.current_url,
                "title": self.driver.title
            }
            
        except Exception as e:
            logger.error(f"Ошибка при получении HTML: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_all_text(self, visible_only: bool = True) -> Dict[str, Any]:
        """
        Получение всего текстового содержимого страницы.
        
        Args:
            visible_only: Получить только видимый текст
        """
        try:
            if not self.driver:
                return {
                    "success": False,
                    "error": "Браузер не запущен"
                }
            
            if visible_only:
                # Получаем только видимый текст
                text = self.driver.execute_script("""
                    return document.body.innerText;
                """)
            else:
                # Получаем весь текст включая скрытый
                text = self.driver.execute_script("""
                    return document.body.textContent;
                """)
            
            return {
                "success": True,
                "text": text,
                "length": len(text),
                "url": self.driver.current_url
            }
            
        except Exception as e:
            logger.error(f"Ошибка при получении текста: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_elements_info(
        self, 
        selector: str, 
        by: str = "css",
        max_elements: int = 50
    ) -> Dict[str, Any]:
        """
        Получение информации о нескольких элементах.
        
        Args:
            selector: Селектор элементов
            by: Тип селектора
            max_elements: Максимальное количество элементов
        """
        try:
            if not self.driver:
                return {
                    "success": False,
                    "error": "Браузер не запущен"
                }
            
            by_mapping = {
                "css": By.CSS_SELECTOR,
                "xpath": By.XPATH,
                "id": By.ID,
                "name": By.NAME,
                "class": By.CLASS_NAME,
                "tag": By.TAG_NAME
            }
            
            by_type = by_mapping.get(by.lower(), By.CSS_SELECTOR)
            
            elements = self.driver.find_elements(by_type, selector)
            
            # Ограничиваем количество элементов
            elements = elements[:max_elements]
            
            elements_data = []
            for idx, element in enumerate(elements):
                try:
                    elements_data.append({
                        "index": idx,
                        "tag": element.tag_name,
                        "text": element.text[:200] if element.text else "",  # Ограничиваем длину
                        "visible": element.is_displayed(),
                        "enabled": element.is_enabled(),
                        "attributes": {
                            "id": element.get_attribute("id"),
                            "class": element.get_attribute("class"),
                            "href": element.get_attribute("href"),
                            "src": element.get_attribute("src"),
                            "type": element.get_attribute("type"),
                            "value": element.get_attribute("value"),
                        }
                    })
                except:
                    # Пропускаем элементы с ошибками
                    continue
            
            return {
                "success": True,
                "count": len(elements_data),
                "elements": elements_data,
                "selector": selector
            }
            
        except Exception as e:
            logger.error(f"Ошибка при получении информации об элементах: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_page_structure(self) -> Dict[str, Any]:
        """
        Получение структурированной информации о странице.
        Возвращает заголовки, ссылки, формы, изображения и т.д.
        """
        try:
            if not self.driver:
                return {
                    "success": False,
                    "error": "Браузер не запущен"
                }
            
            structure = self.driver.execute_script("""
                return {
                    url: window.location.href,
                    title: document.title,
                    headings: {
                        h1: Array.from(document.querySelectorAll('h1')).map(h => h.textContent.trim()).slice(0, 10),
                        h2: Array.from(document.querySelectorAll('h2')).map(h => h.textContent.trim()).slice(0, 20),
                        h3: Array.from(document.querySelectorAll('h3')).map(h => h.textContent.trim()).slice(0, 20)
                    },
                    links: Array.from(document.querySelectorAll('a[href]')).slice(0, 50).map(a => ({
                        text: a.textContent.trim().substring(0, 100),
                        href: a.href,
                        internal: a.hostname === window.location.hostname
                    })),
                    images: Array.from(document.querySelectorAll('img[src]')).slice(0, 30).map(img => ({
                        src: img.src,
                        alt: img.alt
                    })),
                    forms: Array.from(document.querySelectorAll('form')).slice(0, 10).map(form => ({
                        action: form.action,
                        method: form.method,
                        inputs: Array.from(form.querySelectorAll('input, textarea, select')).map(input => ({
                            type: input.type,
                            name: input.name,
                            id: input.id,
                            placeholder: input.placeholder
                        }))
                    })),
                    meta: {
                        description: document.querySelector('meta[name="description"]')?.content || '',
                        keywords: document.querySelector('meta[name="keywords"]')?.content || '',
                        viewport: document.querySelector('meta[name="viewport"]')?.content || ''
                    }
                };
            """)
            
            return {
                "success": True,
                "structure": structure
            }
            
        except Exception as e:
            logger.error(f"Ошибка при получении структуры страницы: {e}")
            return {
                "success": False,
                "error": str(e)
            }
