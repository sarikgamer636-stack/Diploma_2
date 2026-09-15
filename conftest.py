import pytest
from helpers.api import *

@pytest.fixture
def created_user():
    payload = build_user_payload()
    response = register_user(payload)
    token = response.json().get("accessToken")

    yield payload, response
    delete_user(token)