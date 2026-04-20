from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    """Базовый класс для всех страниц"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, url):
        """Открыть страницу по URL"""
        self.driver.get(url)

    def find_element(self, locator):
        """Найти элемент с явным ожиданием"""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        """Кликнуть по элементу"""
        self.find_element(locator).click()

    def input_text(self, locator, text):
        """Ввести текст в поле"""
        field = self.find_element(locator)
        field.clear()
        field.send_keys(text)

    def get_text(self, locator):
        """Получить текст элемента"""
        return self.find_element(locator).text

    def is_element_present(self, locator):
        """Проверить наличие элемента"""
        try:
            self.find_element(locator)
            return True
        except:
            return False

    def get_element_attribute(self, locator, attribute):
        """Получить атрибут элемента"""
        return self.find_element(locator).get_attribute(attribute)