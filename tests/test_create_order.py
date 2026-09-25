from helpers.api import *
from helpers.data import *

@allure.epic("API Stellar Burgers")
@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Проверка: создания заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth_and_ingredients(self, created_user):
        payload, register_response = created_user
        token = register_response.json()["accessToken"]
        ingredients = get_ingredient_ids()[:2]
        response = create_order(ingredients, token)
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert "number" in body["order"]

    @allure.title("Проверка: можно-ли создать заказ без авторизации")
    def test_create_order_without_auth(self):
        ingredients = get_ingredient_ids()[:2]
        response = create_order(ingredients)
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert "number" in body["order"]

    @allure.title("Проверка: нельзя создать заказ без ингредиентов")
    def test_create_order_without_ingredients(self, created_user):
        payload, register_response = created_user
        token = register_response.json()["accessToken"]
        response = create_order([], token)
        assert response.status_code == 400
        assert response.json()["message"] == "Ingredient ids must be provided"

    @allure.title("Проверка: нельзя создать заказ с неверным хешем ингредиента")
    def test_create_order_with_invalid_hash(self, created_user):
        payload, register_response = created_user
        token = register_response.json()["accessToken"]
        response = create_order([INVALID_INGREDIENT_HASH], token)
        assert response.status_code == 500