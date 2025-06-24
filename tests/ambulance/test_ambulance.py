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

