# tests/conftest.py

from dotenv import load_dotenv
import os
import pytest
import requests

load_dotenv()  # načíta .env súbor

BASE_URL = "https://veterinarik.test.aleron.sk"

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

@pytest.fixture(scope="session")
def auth_headers(base_url):
    """
    Fixture na získanie autentizačného tokenu pre testy.
    """
    username = os.getenv("TEST_USERNAME")
    password = os.getenv("TEST_PASSWORD")

    response = requests.get(f"{base_url}/api/login", auth=(username, password))
    assert response.status_code == 200
    token = response.json().get("access_token") or response.json().get("token")
    return {"Authorization": f"Bearer {token}"}
