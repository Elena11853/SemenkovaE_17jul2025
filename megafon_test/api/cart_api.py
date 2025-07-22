import requests
import pytest
import allure
import config_api


class ApiFixture:
    def __init__(self):
        """ Инициализация заголовков HTTP-запросов 
        и токенов аутентификации. 
        Получение текущего заказа клиента. """
        self._headers = {
            "Accept": "application/json",
        }
        self._headers["Cookie"] = f"_ejwt={config_api.EJWT};"
        self._order = self.get_current_order()

    @allure.step("Добавление товара в корзину")
    def add_product(self, product_id: int = 196914):
        """ Добавляет товар в корзину пользователя. 
        :param product_id: ID добавляемого товара. 
        :return: Response объект с результатом операции. """
        try:
            url = f'{config_api.API_URL}{config_api.ADD_PRODUCT_URL}'
            json = {
                "operations": [
                    {
                        "operation": "OrderAddGoodToBasket",
                        "arguments": {
                            "goodId": product_id,
                            "quantity": 1
                        }
                    }
                ]       
            }
            response = requests.post(url, json=json, headers=self._headers)

            self._position = self.get_products_in_order_by_id(product_id)[0]['position']
            return response
        except Exception as e:
            pytest.fail(f"Ошибка добавления товара: {e}")

    @allure.step("Удаление товара из корзины")
    def delete_products(self):
        """ Удаляет товар из корзины пользователя."""
        order_id = self._order['orderId']
        client_id = self._order['clientId']

        url = (
            f"{config_api.CART_URL}order/{order_id}" 
            f"/basket/{self._position}/remove?clientId={client_id}&&cityId=1817"
        )

        headers = self._headers.copy()
        headers["X-Host"] = "vologda.shop.megafon.ru"
        response = requests.delete(url, headers=headers)

        return response

    @allure.step("Обновление количества товара в корзине")
    def update_quantity(self, new_quantity: int):
        """ Обновляет количество выбранного товара в корзине. 
        :param new_quantity: Новое количество товара. """
        try:
            url = (
                f"{config_api.CART_URL}order/{self._order['orderId']}"
                f"/basket/{self._position}/quantity"
                f"?clientId={self._order['clientId']}&cityId=1432"
            )
            payload = {"quantity": new_quantity}
            headers = self._headers.copy()
            headers["X-Host"] = "vologda.shop.megafon.ru"
            response = requests.patch(url, json=payload, headers=headers)

            return response
        except Exception as e:
            pytest.fail(f"Ошибка обновления количества товара: {e}")

    @allure.step("Получение информации о текущем заказе")
    def get_current_order(self):
        url = 'https://api.shop.megafon.ru/eshop/checkout/v2/order/info'
        headers = self._headers.copy()
        headers["X-Host"] = "vologda.shop.megafon.ru"
        response = requests.get(url, headers=headers)

        response_json = response.json()
        return response_json['payload']['order']

    @allure.step("Получение списка товаров в корзине по ID продукта")
    def get_products_in_order_by_id(self, id: int):
        order = self.get_current_order()

        if order == None:
            return None

        products = order['basket']['items']
        if len(products) == 0:
            return None
        
        products_list_by_id = list(filter(lambda x: x['cart']['goodId'] == id, products))
        if len(products_list_by_id) > 0:
            return products_list_by_id
        else:
            return None

    @allure.step("Подсчет общего количества товара в корзине по ID продукта")
    def calc_products_in_cart_by_id(self, id: int):
        """ Подсчитывает общее количество конкретного товара в корзине. 
        :param id: ID товара. :return: Количество товара в корзине. """
        products = self.get_products_in_order_by_id(id)
        if products == None:
            return 0

        count = 0
        for product in products:
            count = count + product['amount']

        return count
    