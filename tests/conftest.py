import pytest
import requests
import os
from dotenv import load_dotenv
import random
import string
import requests

# Načítaj .env súbor
load_dotenv()

BASE_URL = os.getenv("BASE_URL")
USERNAME = os.getenv("TEST_USERNAME")
PASSWORD = os.getenv("TEST_PASSWORD")


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def auth_headers(base_url):
    """
    Fixture na získanie autentifikačného tokenu. Ak login zlyhá, pokúsi sa o registráciu.
    """
    response = requests.get(f"{base_url}/api/login", auth=(USERNAME, PASSWORD))

    if response.status_code != 200:
        # Registruj používateľa
        payload = {
            "id": 0,
            "email": USERNAME,
            "password": PASSWORD,
            "confirm": PASSWORD
        }
        reg_response = requests.post(f"{base_url}/api/register", json=payload)
        assert reg_response.status_code == 200, f"Registrácia zlyhala: {reg_response.text}"

        # Zopakuj login
        response = requests.get(f"{base_url}/api/login", auth=(USERNAME, PASSWORD))

    assert response.status_code == 200, f"Login zlyhal: {response.text}"
    token = response.json().get("access_token") or response.json().get("token")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="session")
def test_owner_id():
    return int(os.getenv("TEST_OWNER_ID", "0"))


@pytest.fixture(scope="session")
def test_vet_id():
    return int(os.getenv("TEST_VET_ID", "0"))

@pytest.fixture(scope="session")
def registered_user_credentials(base_url):
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    login = f"autotest_{suffix}@example.com"
    password = "SilneHeslo123!"

    response = requests.post(f"{base_url}/api/register", json={
        "name": f"AutoTest {suffix}",
        "login": login,
        "password": password
    })

    assert response.status_code == 200, "❌ Registrácia používateľa zlyhala"
    return login, password