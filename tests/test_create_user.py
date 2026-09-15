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

        assert response.status_code == 200
        assert body["success"] is True
        assert body["user"]["email"] == payload["email"]
        assert body["user"]["name"] == payload["name"]
        assert "accessToken" in body

    @allure.title("Проверка: Нельзя создать пользователя, который уже зарегистрирован")
    def test_create_already_registered_user(self, created_user):
        payload, first_response = created_user
        second_response = register_user(payload)

        assert second_response.status_code == 403
        assert second_response.json()["message"] == "User already exists"

    @allure.title("Проверка: Нельзя создать пользователя без заполненного обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_without_required_field(self, missing_field):
        payload = build_user_payload()
        payload.pop(missing_field)
        response = requests.post(REGISTER, json=payload, timeout=20)

        assert response.status_code == 403
        assert response.json()["message"] == "Email, password and name are required fields"