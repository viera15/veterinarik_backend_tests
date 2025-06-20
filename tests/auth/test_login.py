# tests/auth/test_login.py

import os
import requests

class TestLogin:
    def test_status_code(self, base_url):
        response = requests.get(
            f"{base_url}/api/login",
            auth=(os.getenv("TEST_USERNAME"), os.getenv("TEST_PASSWORD"))
        )
        assert response.status_code == 200

    def test_token_present(self, base_url):
        response = requests.get(
            f"{base_url}/api/login",
            auth=(os.getenv("TEST_USERNAME"), os.getenv("TEST_PASSWORD"))
        )
        data = response.json()
        assert "access_token" in data or "token" in data
        assert isinstance(data.get("access_token") or data.get("token"), str)

