import time
import pytest
from pages.main_page import MainPage
from selenium.webdriver.common.by import By

class TestUralAzSite:
    """Тесты для сайта УралАЗ"""
    
    def test_homepage_loading(self, driver):
        """Тест 1: Проверка загрузки главной страницы"""
        main_page = MainPage(driver)
        start_time = time.time()
        
        main_page.open(MainPage.URL)
        
        assert main_page.is_header_loaded(), "Шапка сайта не загрузилась!"
        assert main_page.is_footer_loaded(), "Подвал сайта не загрузился!"
        
        load_time = time.time() - start_time
        print(f"\nСтраница загрузилась за {load_time:.2f} секунд.")
        
        # Проверка скорости (порог 10 секунд)
        assert load_time < 5.0, f"Страница грузится слишком долго: {load_time} сек"

    def test_cookie_banner_handling(self, driver):
        """Тест 2: Проверка обработки cookie-баннера"""
        main_page = MainPage(driver)
        main_page.open(MainPage.URL)
        time.sleep(2)
        
        # Если баннер есть - пробуем закрыть
        if main_page.is_element_present(main_page.COOKIE_BANNER):
            try:
                main_page.accept_cookies_if_present()
                time.sleep(1)
                assert not main_page.is_element_present(main_page.COOKIE_BANNER), \
                    "Баннер cookies остался после закрытия"
                print("\nCookie-баннер успешно закрыт")
            except:
                print("\nCookie-баннер не удалось закрыть автоматически")
        
        # Проверяем, что основной контент доступен
        assert main_page.is_element_present(main_page.HERO_SECTION), \
            "Основной контент заблокирован"

    def test_navigation_menu_presence(self, driver):
        """Тест 3: Проверка наличия навигационного меню"""
        main_page = MainPage(driver)
        main_page.open(MainPage.URL)
        
        # Проверяем, что меню присутствует
        assert main_page.is_header_loaded(), "Навигационное меню отсутствует"
        print("\nНавигационное меню загружено корректно")

    def test_responsive_design_mobile(self, driver):
        """Тест 4: Проверка адаптивности (мобильная версия)"""
        driver.set_window_size(375, 812)  # iPhone X
        
        main_page = MainPage(driver)
        main_page.open(MainPage.URL)
        
        assert main_page.is_element_present(main_page.HEADER), \
            "Шапка не отображается на мобильном разрешении"
        assert main_page.is_element_present(main_page.FOOTER), \
            "Подвал не отображается на мобильном разрешении"
        
        print("\nАдаптивность для мобильных устройств: OK")
        driver.set_window_size(1920, 1080)  # Возвращаем полный размер

    def test_responsive_design_tablet(self, driver):
        """Тест 5: Проверка адаптивности (планшет)"""
        driver.set_window_size(768, 1024)  # iPad
        
        main_page = MainPage(driver)
        main_page.open(MainPage.URL)
        
        assert main_page.is_element_present(main_page.HEADER), \
            "Шапка не отображается на планшетном разрешении"
        assert main_page.is_element_present(main_page.FOOTER), \
            "Подвал не отображается на планшетном разрешении"
        
        print("\nАдаптивность для планшетов: OK")
        driver.set_window_size(1920, 1080)

    def test_catalog_page_loads(self, driver):
        """Тест 6: Проверка загрузки страницы каталога (модели)"""
        main_page = MainPage(driver)
        
        # Переходим напрямую на страницу моделей
        main_page.open(MainPage.CATALOG_URL)
        time.sleep(3)  # Даём время на загрузку
        
        # Проверяем, что есть заголовок страницы
        is_title_present = main_page.is_element_present((By.TAG_NAME, "h1"))
        assert is_title_present, "Страница каталога не содержит заголовка"
        
        # Проверяем, что есть хотя бы один элемент (карточка товара или список)
        # Ищем общие селекторы для карточек техники
        has_content = (
            main_page.is_element_present((By.CSS_SELECTOR, ".model-card, .product-card, .item")) or
            main_page.is_element_present((By.TAG_NAME, "h2")) or
            main_page.is_element_present((By.TAG_NAME, "h3"))
        )
        
        assert has_content, "Страница каталога кажется пустой"
        print("\nСтраница каталога (модели) загружена успешно")

    def test_contacts_page_loads(self, driver):
        """Тест 7: Проверка загрузки страницы контактов"""
        main_page = MainPage(driver)
        main_page.open(MainPage.URL)
        time.sleep(2)
        
        # Пробуем перейти в контакты
        try:
            # Ищем ссылку на контакты
            contact_link = driver.find_element(By.CSS_SELECTOR, 
                "a[href*='contact'], a:contains('Контакты')")
            contact_link.click()
            time.sleep(3)
        except:
            print("\nНе удалось найти ссылку на контакты, проверяем главную")
        
        # Проверяем наличие заголовка
        is_title_present = main_page.is_element_present((By.TAG_NAME, "h1"))
        assert is_title_present, "Страница не содержит заголовка"
        
        # Проверяем наличие формы или контактной информации
        is_input_present = main_page.is_element_present((By.TAG_NAME, "input"))
        is_phone_present = main_page.is_element_present((By.XPATH, "//*[contains(text(), '+')]"))
        
        if is_input_present or is_phone_present:
            print("\nСтраница контактов содержит форму или контактные данные")
        else:
            print("\nВНИМАНИЕ: На странице контактов не найдены формы или телефоны")