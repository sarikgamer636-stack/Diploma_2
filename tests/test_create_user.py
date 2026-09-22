import pytest
from helpers.api import *
from helpers.urls import *

@allure.epic("API Stellar Burgers")
@allure.feature("Создание пользователя")
class TestCreateUser:

    @allure.title("Проверка: можно-ли создать пользователя")
    def test_create_unique_user(self, created_user):
        payload, response = created_user
        body = response.json()

        with allure.step("Проверяем код и тело ответа"):
            assert response.status_code == 200
            assert body["success"] is True
        with allure.step("Проверяем поля email и name"):
            assert body["user"]["email"] == payload["email"]
            assert body["user"]["name"] == payload["name"]
        with allure.step("Проверяем создание токена"):
            assert "accessToken" in body

    @allure.title("Проверка: Нельзя создать пользователя, который уже зарегистрирован")
    def test_create_already_registered_user(self, created_user):
        payload, first_response = created_user
        with allure.step("Пробуем отправить данные уже зарегистрированного пользователя"):
            second_response = register_user(payload)

        with allure.step("Проверяем код ошибки и сообщение об ошибке в теле ответа"):
            assert second_response.status_code == 403
            assert second_response.json()["message"] == "User already exists"

    @allure.title("Проверка: Нельзя создать пользователя без заполненного обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_without_required_field(self, missing_field):
        with allure.step("Пробуем создать пользователя без заполненного обязательного поля"):
            payload = build_user_payload()
            payload.pop(missing_field)
        with allure.step("Отправляем запрос для регистрации"):
            response = requests.post(REGISTER, json=payload, timeout=20)
        with allure.step("Проверяем код и тело ответа"):
            assert response.status_code == 403
            assert response.json()["message"] == "Email, password and name are required fields"