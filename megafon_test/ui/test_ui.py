import pytest
from selenium import webdriver
from cart_ui import PageFixture
import allure


# Создаем браузер
@pytest.fixture(scope="session")
def driver():
    with allure.step("Запуск браузера"):
        _driver = webdriver.Chrome()
        _driver.maximize_window()

    yield _driver
    with allure.step("Завершение сессии браузера"):
        _driver.quit()

@pytest.fixture
def page_fixture(driver):
    with allure.step("Создание объекта PageFixture и открытие главной страницы"):
        _page_fixture = PageFixture(driver)
        _page_fixture.open_site()
        return _page_fixture

@allure.epic("UI Тестирование")
@allure.feature("Корзина покупателя")
@allure.story("Проверка функционала добавления товаров в корзину")
@allure.title("Добавление одного товара в корзину")
@allure.description("Проверка, что товар добавляется в корзину без ошибок.")
def test_add_product(page_fixture):
    page_fixture.add_product_to_cart()
    page_fixture.go_to_cart()

    products_count = page_fixture.get_products_count()
    assert products_count == '1', 'Количество товара должно равняться "1"'

@allure.epic("UI Тестирование")
@allure.feature("Корзина покупателя")
@allure.story("Проверка функционала добавления нескольких товаров в корзину")
@allure.title("Добавление двух товаров в корзину")
@allure.description("Проверка, что товар добавляется в корзину без ошибок.")
def test_add_product_in_cart(page_fixture):
    page_fixture.add_product_to_cart()
    page_fixture.go_to_cart()

    page_fixture.add_product_in_cart()
    products_count = page_fixture.get_products_count()
    assert products_count == '2', 'Количество товара должно равняться "2"'
