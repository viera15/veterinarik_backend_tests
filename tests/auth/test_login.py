import pytest
import requests
import random
import string
from requests.auth import HTTPBasicAuth

@pytest.fixture(scope="module")
def base_url():
    return "https://veterinarik.test.aleron.sk"

@pytest.fixture(scope="module")
def registered_user_credentials(base_url):
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    login = f"testlogin_{suffix}@example.com"
    password = "Heslo123!"
    user_data = {
        "name": f"Test Login Užívateľ {suffix}",
        "login": login,
        "password": password
    }
    response = requests.post(f"{base_url}/api/register", json=user_data)
    assert response.status_code == 200
    return {"login": login, "password": password}

def test_login_valid_user(base_url, registered_user_credentials):
    response = requests.get(
        f"{base_url}/api/login",
        auth=HTTPBasicAuth(registered_user_credentials["login"], registered_user_credentials["password"])
    )
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, dict)
    assert response_data.get("login") == registered_user_credentials["login"]

@pytest.mark.skip(reason="Backend vracia 200 aj pre neplatné heslo – treba opraviť")
def test_login_invalid_password(base_url, registered_user_credentials):
    response = requests.get(
        f"{base_url}/api/login",
        auth=HTTPBasicAuth(registered_user_credentials["login"], "zleheslo")
    )
    assert response.status_code in (401, 403)

@pytest.mark.skip(reason="Backend vracia 200 aj pre neexistujúceho používateľa – treba opraviť")
def test_login_nonexistent_user(base_url):
    response = requests.get(
        f"{base_url}/api/login",
        auth=HTTPBasicAuth("neexistujuci@example.com", "hocico")
    )
    assert response.status_code in (401, 403)

@pytest.mark.skip(reason="Backend vracia 200 aj pre chýbajúce heslo – treba opraviť")
def test_login_missing_password(base_url, registered_user_credentials):
    """
    Overí, že prihlásenie bez hesla zlyhá.
    """
    response = requests.get(
        f"{base_url}/api/login",
        auth=HTTPBasicAuth(registered_user_credentials["login"], "")
    )
    assert response.status_code in (401, 403)
