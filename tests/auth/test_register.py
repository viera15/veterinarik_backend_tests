import requests
import random
import string
import pytest


class TestRegisterUser:

    def generate_unique_user(self):
        """ 
        Vytvorí unikátneho testovacieho používateľa s náhodným emailom. 
        Používa email ako login, čo je vyžadované frontendovou aplikáciou."""
        suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        email = f"testuser_{suffix}@example.com"
        return {
            "name": f"Testovací Používateľ {suffix}",
            "login": email,               # <- login = email
            "email": email,               # <- frontend ho vyžaduje
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
    def test_register_invalid_user(self, base_url):
        """
        Overí, že registrácia neprejde pri nevalidných dátach.
        """
        invalid_data = {
            "name": "Neplatný Používateľ",
            "login": "nevalidny@example.com"
        }

        response = requests.post(f"{base_url}/api/register", json=invalid_data)

        assert response.status_code == 422, "Očakávaný HTTP 422 (Unprocessable Entity) pri chýbajúcich údajoch"
        
        response_data = response.json()
        assert isinstance(response_data, dict), "Očakávaný JSON objekt"
        assert "detail" in response_data, "Chýba detail validácie"
        
        # Môžeš si overiť aj konkrétnu chybu:
        assert any(
            "password" in error.get("loc", []) for error in response_data["detail"]
        ), "Správa neobsahuje chybu pre pole 'password'"


    def test_register_duplicate_user(self, base_url):
        """
        Overí, že registrácia neprejde, ak používateľ už existuje.
        """
        suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        login = f"duplicate_{suffix}@example.com"
        password = "SilneHeslo123!"

        user_data = {
            "name": f"Testovací Duplikát {suffix}",
            "login": login,
            "password": password
        }

        first_response = requests.post(f"{base_url}/api/register", json=user_data)
        assert first_response.status_code == 200
        assert first_response.json().get("status") in ("ok", "registred")

        second_response = requests.post(f"{base_url}/api/register", json=user_data)
        assert second_response.status_code == 200
        assert second_response.json().get("status") == "exists"

   

    @pytest.mark.skip(reason="Backend zatiaľ nevaliduje login ako email")
    def test_register_invalid_login_format(self, base_url):
        """
        Overí, že registrácia neprejde, ak login nie je vo forme emailu.
        """
        invalid_data = {
            "name": "Zlý Login",
            "login": "neplatny_login_bez_zavinaca",
            "password": "Heslo123!"
        }

        response = requests.post(f"{base_url}/api/register", json=invalid_data)

        assert response.status_code in (400, 422), "Očakávaná chyba pri zlom formáte loginu"
        response_data = response.json()
        assert isinstance(response_data, dict)
        assert "detail" in response_data

    def test_register_short_password(self, base_url):
        """
        Overí, že registrácia neprejde, ak je heslo príliš krátke.
        """
        invalid_data = {
            "name": "Krátke Heslo",
            "login": f"shortpass{random.randint(1000,9999)}@example.com",
            "password": "12"
        }

        response = requests.post(f"{base_url}/api/register", json=invalid_data)

        assert response.status_code in (400, 422), "Očakávaná chyba pri krátkom hesle"
        response_data = response.json()
        assert isinstance(response_data, dict)
        assert "detail" in response_data

    @pytest.mark.skip(reason="Backend zatiaľ nevaliduje silu hesla")
    def test_register_weak_password(self, base_url):
        """
        Overí, že registrácia neprejde, ak je heslo príliš slabé.
        """
        invalid_data = {
            "name": "Slabé Heslo",
            "login": f"weakpass{random.randint(1000,9999)}@example.com",
            "password": "1234567"  # 7 znakov, bez písmen/špeciálnych znakov
        }

        response = requests.post(f"{base_url}/api/register", json=invalid_data)

        assert response.status_code in (400, 422), "Očakávaná chyba pri slabom hesle"
        response_data = response.json()
        assert isinstance(response_data, dict)
        assert "detail" in response_data
