from helpers.api import *

@allure.epic("API Stellar Burgers")
@allure.feature("Логин пользователя")
class TestLogin:

    @allure.title("Проверка: Можно войти под существующим пользователем")
    def test_login_existing_user(self, created_user):
        payload, register_response = created_user
        with allure.step("Логинимся"):
            response = login_user(payload["email"], payload["password"])
            body = response.json()

        with allure.step("Проверяем код и тело ответа"):
            assert response.status_code == 200
            assert body["success"] is True
        with allure.step("Проверяем данные пользователя и полученный токен в теле ответа"):
            assert body["user"]["email"] == payload["email"]
            assert "accessToken" in body

    @allure.title("Проверка: Нельзя войти с неверным паролем")
    def test_login_with_wrong_credentials(self, created_user):
        payload, register_response = created_user
        with allure.step("Пробуем залогиниться с неверным паролем"):
            response = login_user(payload["email"], "wrong_password")

        with allure.step("Проверяем код и сообщение об ошибке в теле ответа"):
            assert response.status_code == 401
            assert response.json()["message"] == "email or password are incorrect"