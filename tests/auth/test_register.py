import requests
import random
import string
import pytest


class TestRegisterUser:

    def generate_unique_user(self):
        suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        return {
            "name": f"Testovací Používateľ {suffix}",
            "login": f"test_user_{suffix}",
            "password": "Heslo123!"
        }

    def test_register_valid_user(self, base_url):
        """
        Otestuje registráciu nového používateľa cez /api/register
        """
        user_data = self.generate_unique_user()

        response = requests.post(
            f"{base_url}/api/register",
            json=user_data
        )

        assert response.status_code == 200, f"Chyba: {response.status_code} - {response.text}"

        response_data = response.json()
        assert isinstance(response_data, dict), "Očakávaný JSON objekt"
        # Podľa odpovede môžeš kontrolovať napr. "status": "ok"
        # assert response_data.get("status") == "ok"

        # 👉 voliteľne: ulož prihlasovacie údaje pre ďalšie testy
        self.login = user_data["login"]
        self.password = user_data["password"]
