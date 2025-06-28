# tests/ambulance/test_ambulance.py
import pytest
import requests
import random
import os
import sys

# nastav koreňový adresár (tam, kde je `utils`)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from veterinarik_backend_tests.utils.api_helpers import extract_items, is_security_restricted


class TestAmbulance:

    def test_get_ambulance_list(self, base_url, auth_headers):
        """
        Otestuje GET /api/ambulance – získa zoznam ambulancií.
        """
        response = requests.get(f"{base_url}/api/ambulance", headers=auth_headers)
        if is_security_restricted(response):
            pytest.skip("🔐 Používateľ nemá oprávnenie čítať ambulancie.")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list) or isinstance(data, dict)

    def test_post_ambulance_invalid(self, base_url, auth_headers):
        """
        Otestuje POST /api/ambulance s nevalidnými dátami – očakávame 422.
        """
        payload = {
            "id": None,
            "owner_id": None,
            "title": ""
        }
        response = requests.post(
            f"{base_url}/api/ambulance",
            json=payload,
            headers=auth_headers
        )
        assert response.status_code == 422

    def test_post_ambulance_valid(self, base_url, auth_headers, test_owner_id):
        """
        Otestuje vytvorenie ambulancie. Otestuje POST /api/ambulance s validnými dátami.
        """
        payload = {
            "id": 0,  # ID sa má nastaviť automaticky
            "owner_id": test_owner_id,
            "title": f"Test ambulancia {random.randint(1000, 9999)}",
            "description": "Automatický testovací zápis"
        }

        response = requests.post(
            f"{base_url}/api/ambulance",
            json=payload,
            headers=auth_headers
        )

        if is_security_restricted(response):
            pytest.skip("🔐 Používateľ nemá oprávnenie na vytváranie ambulancií.")

        assert response.status_code == 200, f"❌ Neočakávaný status: {response.status_code}, odpoveď: {response.text}"

        data = response.json()
        assert data.get("status") in ("ok", "exists"), f"❌ Neočakávaný 'status': {data}"

    def test_post_ambulance_edit_existing(self, base_url, auth_headers, test_owner_id):
        """
        Otestuje POST /api/ambulance – úprava existujúcej ambulancie.
        """
        # Najprv vytvoríme ambulanciu
        create_payload = {
            "id": 0,
            "owner_id": test_owner_id,
            "title": f"Ambulancia na úpravu {random.randint(1000, 9999)}",
            "description": "Pôvodný popis"
        }
        create_resp = requests.post(f"{base_url}/api/ambulance", json=create_payload, headers=auth_headers)
        if is_security_restricted(create_resp):
            pytest.skip("🔐 Používateľ nemá oprávnenie na vytváranie ambulancií.")
        assert create_resp.status_code == 200
        created = create_resp.json()
        assert created.get("status") == "ok"
        ambulance_id = created.get("id") or created.get("ambulance", {}).get("id")
        assert ambulance_id, "❌ Ambulancia nebola správne vytvorená"

        # Teraz ambulanciu upravíme – stále cez POST
        update_payload = {
            "id": ambulance_id,
            "owner_id": test_owner_id,
            "title": f"Upravená ambulancia {random.randint(1000, 9999)}",
            "description": "Toto je upravený popis"
        }
        update_resp = requests.post(f"{base_url}/api/ambulance", json=update_payload, headers=auth_headers)
        assert update_resp.status_code == 200, f"❌ Neočakávaný status {update_resp.status_code}, odpoveď: {update_resp.text}"
        updated = update_resp.json()
        assert updated.get("status") == "ok", f"❌ Očakávaný status 'ok', odpoveď: {updated}"

    def test_put_ambulance_unauthorized_user(self, base_url, auth_headers, test_owner_id):
        """
        Otestuje, že používateľ nemôže upraviť cudziu ambulanciu (očakávame 403 alebo podobný zákaz).
        """
        # Vytvoríme ambulanciu ako aktuálny používateľ
        create_payload = {
            "id": 0,
            "owner_id": test_owner_id,
            "title": f"Ambulancia iného používateľa {random.randint(1000,9999)}",
            "description": "Na test neoprávnenej úpravy"
        }
        create_resp = requests.post(f"{base_url}/api/ambulance", json=create_payload, headers=auth_headers)
        if is_security_restricted(create_resp):
            pytest.skip("🔐 Používateľ nemá oprávnenie vytvárať ambulanciu.")

        assert create_resp.status_code == 200
        created = create_resp.json()
        ambulance_id = created.get("id") or created.get("ambulance", {}).get("id")
        assert ambulance_id, "❌ Ambulancia nebola správne vytvorená"

        # Teraz použijeme iný token (nového používateľa)
        other_user_token = self.create_temp_token(base_url)
        other_headers = {
            "Authorization": f"Bearer {other_user_token}"
        }

        # Pokus o úpravu cudzej ambulancie
        update_payload = {
            "id": ambulance_id,
            "owner_id": 99999,  # Úmyselne neexistujúci alebo cudzí vlastník
            "title": "Neoprávnená úprava",
            "description": "Zlá úprava"
        }
        update_resp = requests.post(f"{base_url}/api/ambulance", json=update_payload, headers=other_headers)

        assert update_resp.status_code in (403, 401), f"❌ Neočakávaný status: {update_resp.status_code}, odpoveď: {update_resp.text}"

    def create_temp_token(self, base_url):
        """
        Pomocná funkcia na vytvorenie tokenu pre iného používateľa.
        """
        suffix = random.randint(10000, 99999)
        login = f"unauth{suffix}@example.com"
        password = "Heslo123!"

        reg_data = {
            "name": f"Neoprávnený {suffix}",
            "login": login,
            "password": password
        }
        reg_response = requests.post(f"{base_url}/api/register", json=reg_data)
        assert reg_response.status_code == 200

        login_resp = requests.get(f"{base_url}/api/login", auth=(login, password))
        assert login_resp.status_code == 200
        return login_resp.json().get("access_token")


