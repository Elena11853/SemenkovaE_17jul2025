import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import allure
import config_ui


class PageFixture:
    def __init__(self, driver):
        """Инициализация класса SearchPage с драйвером и временем ожидания.

        Args:
            driver (WebDriver): Драйвер Selenium для управления браузером.
        """
        self.driver = driver
        self.wait = WebDriverWait(
            driver, config_ui.WEB_DRIVER_TIMEOUT)

    @allure.step("Удаление всех cookie")
    def clear_cookies(self):
        """ Метод для полной очистки cookies браузера. """
        self.driver.delete_all_cookies()

    @allure.step("поиск элемента по селектору `{selector}` с ожиданием появления его на странице")
    def find_element(self, method, selector):
        """
        Поиск первого на странице элемента по селектору 
        с ожиданием его кликабельности
        Args:
            method: способ поиска (например By.CSS_SELECTOR)
            selector: строка для поиска (например `.my-selector`)
        """
        return self.wait.until(
            ec.element_to_be_clickable((method, selector)))

    @allure.step("Открытие сайта")
    def open_site(self):
        """Очистка cookies перед открытием страницы"""
        self.clear_cookies()
        """Открываем страницу сайта"""
        self.driver.get(config_ui.SITE_URL)

    @allure.step("Переход в корзину") 
    def open_cart(self):
        self.driver.get(config_ui.CART_URL)

    @allure.step("Закрытие браузера")
    def close_site(self):
        self.driver.quit()

    @allure.step("Добавление продукта в корзину")
    def add_product_in_cart(self):
        xpath = './/button[@data-testid="addition-id"]'
        button = self.find_element(By.XPATH, xpath)
        button.click()

    @allure.step("Нажатие кнопки 'В корзину'")
    def add_product_to_cart(self):
        xpath = '//button[text()="В корзину"]'
        buy_button = self.find_element(By.XPATH, xpath)
        buy_button.click()

    @allure.step("Клик по кнопке 'Оформить заказ'")
    def go_to_cart(self):
        button_xpath = '//a[text()="Оформить заказ"]'
        button = self.find_element(By.XPATH, button_xpath)
        button.click()

    @allure.step("Получение количества товаров в корзине")
    def get_products_count(self):
        count_xpath = '/html/body/main/div/div/div/div/div[2]/div[1]/div[1]/div[1]/div[1]/p[1]'
        count_element = self.find_element(By.XPATH, count_xpath)

        """регулярное выражение для выделения числа из строки"""
        re_digits = re.compile(r"\b\d+\b")
        """получаем массив чисел из строки, 
        забираем первый элемент, возвращаем его 
        (в тексте с количеством есть толкьо одна цифра)"""
        print('count of products', re_digits.findall(
            count_element.text)[0])
        return re_digits.findall(count_element.text)[0]
