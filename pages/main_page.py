from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class MainPage(BasePage):
    URL = "https://uralaz.ru"
    
    # ЛОКАТОРЫ
    HEADER = (By.CSS_SELECTOR, "header")
    FOOTER = (By.CSS_SELECTOR, "footer")
    HERO_SECTION = (By.CSS_SELECTOR, "section:first-of-type, .hero, .banner")
    
    # Cookie баннер
    COOKIE_BANNER = (By.CSS_SELECTOR, ".cookie-banner, #cookie-notice, [class*='cookie'], [id*='cookie']")
    CLOSE_COOKIE = (By.CSS_SELECTOR, ".cookie-close, .cookie-accept, button.accept, [class*='accept']")
    
    
    CATALOG_URL = "https://uralaz.ru/models/"  
    CONTACTS_URL = "https://uralaz.ru/contacts/"
    
    def is_header_loaded(self):
        return self.is_element_present(self.HEADER)

    def is_footer_loaded(self):
        return self.is_element_present(self.FOOTER)
    
    def accept_cookies_if_present(self):
        if self.is_element_present(self.COOKIE_BANNER):
            try:
                self.click(self.CLOSE_COOKIE)
            except:
                pass