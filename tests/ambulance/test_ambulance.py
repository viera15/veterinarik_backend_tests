# tests/ambulance/test_ambulance.py

import requests
import random


class TestAmbulance:

    def test_get_ambulance_list(self, base_url, auth_headers):
        """
        Otestuje GET /api/ambulance – získa zoznam ambulancií.
        """
        response = requests.get(f"{base_url}/api/ambulance", headers=auth_headers)
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

    def test_post_ambulance_valid(self, base_url, auth_headers):
        """
        Otestuje POST /api/ambulance s validnými dátami – kontroluje len status odpovede.
        """
        payload = {
            "id": 0,
            "owner_id": 1,  # uprav podľa reálnych testovacích údajov
            "title": f"Test ambulancia {random.randint(1000, 9999)}",
            "description": "Automatický testovací zápis"
        }

        response = requests.post(
            f"{base_url}/api/ambulance",
            json=payload,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("status") in ("ok", "exists")
        assert isinstance(data.get("id"), int)


