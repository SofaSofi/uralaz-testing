import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.download_manager import WDMDownloadManager
from webdriver_manager.core.http import HttpClient

# Класс для обработки сетевых ошибок при загрузке драйвера
class RobustHttpClient(HttpClient):
    def get(self, url, params=None, **kwargs):
        try:
            return super().get(url, params, **kwargs)
        except Exception:
            # Если не удалось скачать — используем кэш или локальный драйвер
            print(f"⚠️ Не удалось загрузить драйвер из {url}, используем кэш...")
            raise

@pytest.fixture(scope="function")
def driver():
    """Фикстура для инициализации WebDriver с обработкой сетевых ошибок"""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    # Отключаем сбор телеметрии для стабильности
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    try:
        # Пытаемся получить драйвер с кэшированием
        driver_path = ChromeDriverManager(
            cache_valid_range=365,  # Кэш драйвера действителен 1 год
            download_manager=WDMDownloadManager(http_client=RobustHttpClient())
        ).install()
        service = Service(driver_path)
    except Exception as e:
        # Фоллбэк: пробуем найти драйвер в системе или использовать путь по умолчанию
        print(f"⚠️ Используем системный ChromeDriver: {e}")
        service = Service()  # Selenium сам попробует найти драйвер в PATH
    
    drv = webdriver.Chrome(service=service, options=options)
    drv.implicitly_wait(10)
    yield drv
    drv.quit()