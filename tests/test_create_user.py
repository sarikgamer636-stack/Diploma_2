import pytest
from helpers.api import *
from helpers.urls import *

@allure.epic("API Stellar Burgers")
@allure.feature("Создание пользователя")
class TestCreateUser:

    @allure.title("Проверка: можно-ли создать пользователя")
    def test_create_unique_user(self):
        payload = build_user_payload()
        response = register_user(payload)
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert body["user"]["email"] == payload["email"]
        assert body["user"]["name"] == payload["name"]
        assert "accessToken" in body

        delete_user(body["accessToken"])

    @allure.title("Проверка: Нельзя создать пользователя, который уже зарегистрирован")
    def test_create_already_registered_user(self, created_user):
        payload, first_response = created_user
        second_response = register_user(payload)

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