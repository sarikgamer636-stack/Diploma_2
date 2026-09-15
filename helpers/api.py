import random
import string
import allure
import requests
from helpers.data import *
from helpers.urls import *

def generate_email():
    letters = string.ascii_lowercase
    suffix = "".join(random.choice(letters) for _ in range(8))
    return f"evg_{suffix}@yandex.ru"

def build_user_payload():
    payload = {
        "email": generate_email(),
        "password": PASSWORD,
        "name": NAME,
    }
    return payload


@allure.step("Регистрируем пользователя")
def register_user(payload):
    return requests.post(REGISTER, json=payload, timeout=20)


@allure.step("Логинимся под пользователем")
def login_user(email, password):
    return requests.post(
        LOGIN,
        json={"email": email, "password": password},
        timeout=20,
    )


@allure.step("Удаляем пользователя после теста")
def delete_user(access_token):
    if not access_token:
        return
    try:
        requests.delete(USER, headers={"Authorization": access_token}, timeout=30)
    except requests.exceptions.RequestException:
        pass


@allure.step("Берем id ингредиентов")
def get_ingredient_ids():
    response = requests.get(INGREDIENTS, timeout=20)
    data = response.json()["data"]
    ids = []
    for item in data:
        ids.append(item["_id"])
    return ids


@allure.step("Создаём заказ")
def create_order(ingredients, token=None):
    headers = {}
    if token:
        headers["Authorization"] = token
    return requests.post(
        ORDERS,
        json={"ingredients": ingredients},
        headers=headers,
        timeout=20,
    )