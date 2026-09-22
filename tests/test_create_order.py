from helpers.api import *
from helpers.data import *

@allure.epic("API Stellar Burgers")
@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Проверка: создания заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth_and_ingredients(self, created_user):
        payload, register_response = created_user
        token = register_response.json()["accessToken"]

        with allure.step("Получаем ингредиенты"):
            ingredients = get_ingredient_ids()[:2]
        with allure.step("Запрос на создание заказа"):
            response = create_order(ingredients, token)
            body = response.json()

        with allure.step("Проверяем код и тело ответа"):
            assert response.status_code == 200
            assert body["success"] is True
        with allure.step("Проверяем номер в теле ответа"):
            assert "number" in body["order"]

    @allure.title("Проверка: можно-ли создать заказ без авторизации")
    def test_create_order_without_auth(self):
        with allure.step("Получаем ингредиенты"):
            ingredients = get_ingredient_ids()[:2]
        with allure.step("Создаем заказ без токена"):
            response = create_order(ingredients)
            body = response.json()

        with allure.step("Проверяем код и тело ответа"):
            assert response.status_code == 200
            assert body["success"] is True
            assert "number" in body["order"]

    @allure.title("Проверка: нельзя создать заказ без ингредиентов")
    def test_create_order_without_ingredients(self, created_user):
        payload, register_response = created_user
        token = register_response.json()["accessToken"]

        with allure.step("Пробуем создать заказ без ингредиентов"):
            response = create_order([], token)
        with allure.step("Проверяем код и текст ошибки в ответе"):
            assert response.status_code == 400
            assert response.json()["message"] == "Ingredient ids must be provided"

    @allure.title("Проверка: нельзя создать заказ с неверным хешем ингредиента")
    def test_create_order_with_invalid_hash(self, created_user):
        payload, register_response = created_user
        token = register_response.json()["accessToken"]
        with allure.step("Отправляем заказ с несуществующим ХЭШЕМ"):
            response = create_order([INVALID_INGREDIENT_HASH], token)
        with allure.step("Проверяем что код ошибки = 500"):
            assert response.status_code == 500