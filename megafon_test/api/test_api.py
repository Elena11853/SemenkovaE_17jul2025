import allure
from cart_api import ApiFixture

apiFixture = ApiFixture()

@allure.epic("API Тестирование")
@allure.feature("Корзина товаров")
@allure.story("Добавление товара в корзину")
@allure.title("Успешное добавление товара в корзину")
@allure.description("Проверка, что товар " \
"добавляется в корзину без ошибок.")
def test_add_product():
    product_id = 196914

    response = apiFixture.add_product(product_id)
    assert response.status_code == 200, 'Не удалось добавить товар'

    products_number = apiFixture.calc_products_in_cart_by_id(product_id)
    assert products_number == 1, f'Должен быть добавлен 1 товар, добавлено {products_number}'
    apiFixture.delete_products()

@allure.epic("API Тестирование")
@allure.feature("Корзина товаров")
@allure.story("Удаление товара из корзины")
@allure.title("Успешное удаление товара из корзины")
@allure.description("Проверка, что товар" \
"удаляется из корзины без ошибок.")
def test_delete_product():
    product_id = 196914

    response = apiFixture.add_product(product_id)
    assert response.status_code == 200, 'Не удалось добавить товар'

    apiFixture.delete_products()

    products_number = apiFixture.calc_products_in_cart_by_id(product_id)
    assert products_number == 0, f'Должен быть добавлен 1 товар, добавлено {products_number}'

@allure.epic("API Тестирование")
@allure.feature("Корзина товаров")
@allure.story("Изменение количества товара в корзине")
@allure.title("Успешное изменение количества товара в корзине")
@allure.description("Проверка, что количество товара в корзине" \
"изменяется без ошибок.")
def test_update_product_quantity():
    product_id = 196914
    new_quantity = 2
    apiFixture.add_product(product_id)
    response = apiFixture.update_quantity(new_quantity)
    assert response.status_code == 200, 'Не удалось добавить товар'
    
    products_number = apiFixture.calc_products_in_cart_by_id(product_id)
    assert products_number == 2, f'Должен быть добавлен 2 товар, добавлено {products_number}'

    apiFixture.delete_products()
