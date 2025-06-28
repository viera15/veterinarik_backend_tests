import random
import pytest
import requests

import os
import sys

# nastav koreňový adresár (tam, kde je `utils`)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from veterinarik_backend_tests.utils.api_helpers import extract_items, is_security_restricted




class TestOwner:

    def test_get_owner_list(self, base_url: str | None, auth_headers: dict[str, str]):
        """
        Otestuje GET /api/owner – získa zoznam ownerov.
        """
        response = requests.get(f"{base_url}/api/owner", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()

        if is_security_restricted(data):
            pytest.skip("🔐 Prístup zamietnutý – test sa preskočí.")

        assert isinstance(data, list)

    def test_post_owner_invalid(self, base_url: str | None, auth_headers: dict[str, str]):
        """
        Otestuje POST /api/owner s nevalidnými dátami – očakávame 422.
        """
        payload = {
            "id": 0,
            "vet_id": None,
            "name": None
        }

        response = requests.post(f"{base_url}/api/owner", json=payload, headers=auth_headers)
        assert response.status_code == 422

    def test_post_owner_valid(self, base_url: str | None, auth_headers: dict[str, str], test_vet_id: int):
        """
        Otestuje POST /api/owner s validnými dátami.
        """
        payload = {
            "id": 0,
            "vet_id": test_vet_id,
            "name": f"Test owner {random.randint(1000, 9999)}",
            "email": "testowner@example.com",
            "phone": "0900123456",
            "description": "Automatický testovací zápis"
        }

        response = requests.post(f"{base_url}/api/owner", json=payload, headers=auth_headers)
        data = response.json()

        if is_security_restricted(data):
            pytest.skip("🔐 Prístup zamietnutý – test sa preskočí.")

        assert response.status_code == 200
        assert data.get("status") in ("ok", "exists")
