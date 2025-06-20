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

    def test_post_ambulance_valid(self, base_url, auth_headers, test_owner_id):
        payload = {
            "id": 0,
            "owner_id": test_owner_id,
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



