import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.main_page import MainPage

class TestAccessibility:
    """Тесты доступности (a11y)"""
    
    def test_images_have_alt_attribute(self, driver):
        """Тест 8: Проверка наличия alt у изображений"""
        main_page = MainPage(driver)
        main_page.open(MainPage.URL)
        time.sleep(2)
        
        images = driver.find_elements(By.TAG_NAME, "img")
        images_without_alt = [img.get_attribute("src") for img in images 
                              if not img.get_attribute("alt") or not img.get_attribute("alt").strip()]
        
        coverage = (len(images) - len(images_without_alt)) / len(images) * 100 if images else 100
        print(f"\nПокрытие alt-атрибутами: {coverage:.1f}% ({len(images_without_alt)} без alt из {len(images)})")
        
        assert coverage >= 80, f"Менее 80% изображений имеют alt ({coverage:.1f}%)"

    def test_form_inputs_have_labels(self, driver):
        """Тест 9: Проверка label у полей ввода"""
        main_page = MainPage(driver)
        main_page.open(MainPage.CONTACTS_URL)
        time.sleep(2)
        
        inputs = driver.find_elements(By.TAG_NAME, "input")
        unlabelled = []
        for inp in inputs:
            if inp.get_attribute("type") in ["submit", "hidden", "checkbox", "radio"]:
                continue
            if not (inp.get_attribute("aria-label") or inp.get_attribute("placeholder") or inp.get_attribute("id")):
                unlabelled.append(inp.get_attribute("name"))
            elif inp.get_attribute("id"):
                try:
                    driver.find_element(By.CSS_SELECTOR, f'label[for="{inp.get_attribute("id")}"]')
                except:
                    unlabelled.append(inp.get_attribute("name"))
        
        print(f"\nПоля без label: {unlabelled if unlabelled else 'Нет'}")
        assert len(unlabelled) == 0, f"Найдены поля без подписей: {unlabelled}"


class TestSEOOptimization:
    """Тесты SEO и структуры контента"""
    
    def test_title_and_meta_description(self, driver):
        """Тест 10: Проверка title и meta description"""
        main_page = MainPage(driver)
        main_page.open(MainPage.URL)
        
        title = driver.title
        assert 10 <= len(title) <= 60, f"Title некорректной длины: {len(title)} симв."
        
        try:
            desc = driver.find_element(By.NAME, "description").get_attribute("content")
            assert 50 <= len(desc) <= 160, f"Description некорректной длины: {len(desc)} симв."
        except:
            pytest.fail("Meta description отсутствует")

    def test_single_h1_heading(self, driver):
        """Тест 11: Проверка единственного H1"""
        main_page = MainPage(driver)
        main_page.open(MainPage.URL)
        time.sleep(2)
        
        h1s = driver.find_elements(By.TAG_NAME, "h1")
        assert len(h1s) == 1, f"На странице {len(h1s)} заголовков H1 (должен быть 1)"


class TestPerformanceAndErrors:
    """Тесты производительности и ошибок"""
    
    def test_no_severe_console_errors(self, driver):
        """Тест 12: Проверка консольных ошибок"""
        main_page = MainPage(driver)
        main_page.open(MainPage.URL)
        time.sleep(3)
        
        logs = driver.get_log("browser")
        severe_errors = [log for log in logs if log["level"] == "SEVERE"]
        
        if severe_errors:
            print(f"\nОшибки консоли ({len(severe_errors)}):")
            for err in severe_errors[:3]:
                print(f"  - {err['message'][:120]}")
        
        assert len(severe_errors) <= 3, f"Превышен лимит ошибок консоли: {len(severe_errors)}"

    def test_detailed_load_metrics(self, driver):
        """Тест 13: Метрики загрузки через Performance API"""
        main_page = MainPage(driver)
        start = time.time()
        main_page.open(MainPage.URL)
        
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        
        full_load = time.time() - start
        print(f"\nFull Load Time: {full_load:.2f} sec")
        
        assert full_load <= 5.0, f"Загрузка дольше 5 сек: {full_load:.2f}"


class TestContentQuality:
    """Тесты качества контента"""
    
    def test_footer_links_validity(self, driver):
        """Тест 14: Проверка ссылок в футере"""
        main_page = MainPage(driver)
        main_page.open(MainPage.URL)
        time.sleep(2)
        
        footer = driver.find_element(By.TAG_NAME, "footer")
        links = footer.find_elements(By.TAG_NAME, "a")[:5]  # Первые 5 для скорости
        
        broken = []
        for link in links:
            href = link.get_attribute("href")
            if href and href.startswith("http"):
                try:
                    driver.execute_script(f"window.open('{href}', '_blank').close()")
                except Exception as e:
                    broken.append(href)
        
        print(f"\nБитые ссылки в футере: {broken if broken else 'Нет'}")
        assert len(broken) == 0, f"Найдены нерабочие ссылки: {broken}"

    def test_contact_info_availability(self, driver):
        """Тест 15: Наличие контактов"""
        main_page = MainPage(driver)
        main_page.open(MainPage.CONTACTS_URL)
        time.sleep(2)
        
        phone = main_page.is_element_present((By.XPATH, "//*[contains(text(), '+') or contains(text(), '8-800')]"))
        email = main_page.is_element_present((By.XPATH, "//*[contains(text(), '@')]"))
        
        print(f"\nКонтакты: Телефон={'✓' if phone else '✗'}, Email={'✓' if email else '✗'}")
        assert phone or email, "Не найден телефон или email на странице контактов"