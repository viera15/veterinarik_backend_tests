# tests/conftest.py
import pytest
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # načítaj premenné z .env

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
USERNAME = os.getenv("TEST_USERNAME")
PASSWORD = os.getenv("TEST_PASSWORD")
OWNER_ID = int(os.getenv("TEST_OWNER_ID", "1"))

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def test_owner_id():
    return OWNER_ID


@pytest.fixture(scope="session")
def auth_headers():
    """
    Fixture na získanie tokenu – použiteľný v každom teste.
    """
    response = requests.get(f"{BASE_URL}/api/login", auth=(USERNAME, PASSWORD))
    assert response.status_code == 200
    token = response.json().get("access_token") or response.json().get("token")
    return {"Authorization": f"Bearer {token}"}
