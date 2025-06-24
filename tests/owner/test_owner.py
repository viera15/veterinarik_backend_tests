import pytest
import requests
import random
import sys
import os

# Pre prístup k helperom
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from utils.api_helpers import extract_items


class TestOwner:

    def test_get_owners(self, base_url, auth_headers):
        response = requests.get(f"{base_url}/api/owner", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()

        if isinstance(data, dict) and (
            data.get("status") == "security" or
            "unauthorized" in data.get("message", "").lower() or
            "access denied" in data.get("message", "").lower()
        ):
            pytest.skip("🔐 Používateľ nemá oprávnenie na čítanie ownerov – test sa preskočí.")

        owners = extract_items(data, key="owners")
        assert isinstance(owners, list), "❌ Očakával sa zoznam ownerov."

    def test_post_owner_valid(self, base_url, auth_headers, test_vet_id):
        payload = {
            "id": 0,
            "vet_id": test_vet_id,
            "name": f"Test owner {random.randint(1000, 9999)}",
            "email": "testowner@example.com",
            "phone": "0900123456",
            "description": "Automatický testovací zápis"
        }

        response = requests.post(
            f"{base_url}/api/owner",
            json=payload,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()

        if data.get("status") == "security":
            pytest.skip("🔐 Prístup zamietnutý – test sa preskočí.")

        assert data.get("status") in ("ok", "exists"), f"❌ Nečakaný status: {data.get('status')}"

    def test_vet_id_exists(self, base_url, auth_headers, test_vet_id):
        response = requests.get(f"{base_url}/api/owner", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()

        if isinstance(data, dict) and (
            data.get("status") == "security" or
            "unauthorized" in data.get("message", "").lower() or
            "access denied" in data.get("message", "").lower()
        ):
            pytest.skip("🔐 Používateľ nemá oprávnenie na čítanie ownerov – test sa preskočí.")

        owners = extract_items(data, key="owners")

        found = any(
            isinstance(owner, dict) and owner.get("vet_id") == test_vet_id
            for owner in owners
        )
        assert found, f"❌ vet_id={test_vet_id} sa nenašiel medzi ownermi"
