# tests/auth/test_login.py

import requests
import os

class TestLogin:
    def test_login_status_code(self, base_url, auth_headers):
        """
        Otestuje GET /api/login – očakávame 200.
        """
        username, password = (
            os.getenv("TEST_USERNAME"),
            os.getenv("TEST_PASSWORD")
        )

        response = requests.get(
            f"{base_url}/api/login",
            auth=(username, password)
        )

        assert response.status_code == 200
        assert response.headers["Content-Type"].startswith("application/json")

    def test_token_response(self, base_url):
        """
        Otestuje, či sa v odpovedi nachádza token.
        """
        username, password = (
            os.getenv("TEST_USERNAME"),
            os.getenv("TEST_PASSWORD")
        )

        response = requests.get(
            f"{base_url}/api/login",
            auth=(username, password)
        )

        assert response.status_code == 200

        data = response.json()
        token = data.get("access_token") or data.get("token")

        assert token, "❌ Token sa nenachádza v odpovedi"
        assert isinstance(token, str), "❌ Token nie je typu string"
        assert len(token) > 10, "❌ Token je podozrivo krátky"

    def test_token_is_valid(self, base_url, auth_headers):
        """
        Overí, že získaný token je platný a dá sa použiť pri volaní chránenej API.
        """
        response = requests.get(
            f"{base_url}/api/ambulance",
            headers=auth_headers
        )
        assert response.status_code == 200, "❌ Token je neplatný alebo endpoint nie je prístupný"
        assert isinstance(response.json(), (list, dict)), "❌ Neočakávaný typ odpovede"
