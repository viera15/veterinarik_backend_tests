import pytest
from utils.db_helpers import (
    get_columns_metadata,
    get_foreign_keys,
    get_primary_key,
)

# Očakávané stĺpce a ich typy podľa reálnej DB (screenshot)
expected_columns = {
    "id": "int",
    "owner_id": "int",
    "title": "varchar",
    "description": "text",
    "status": "int"
}

expected_not_nullable = {
    "id", "owner_id", "title", "status"
}

expected_primary_key = "id"
expected_foreign_keys = {
    ("owner_id", "owner", "id"),
}

def test_ambulance_columns_exist_and_types():
    """Test na overenie existencie stĺpcov a typov stĺpcov tabuľky `ambulance`."""
    cols = {col[0]: col[1] for col in get_columns_metadata("ambulance")}
    for col_name, expected_type in expected_columns.items():
        assert col_name in cols, f"Chýba stĺpec: {col_name}"
        assert expected_type in cols[col_name], f"Typ stĺpca {col_name} má byť {expected_type}, ale je {cols[col_name]}"

def test_ambulance_column_nullability():
    """Test na overenie NOT NULL stĺpcov (nesmie byť prázdny) tabuľky `ambulance`."""
    cols = {col[0]: col[2] for col in get_columns_metadata("ambulance")}
    for col in expected_not_nullable:
        assert cols.get(col) == "NO", f"Stĺpec {col} by mal byť NOT NULL"

def test_ambulance_primary_key():
    """Test na overenie PRIMÁRNEHO kľúča tabuľky `ambulance`."""
    pk = get_primary_key("ambulance")
    assert pk == expected_primary_key, f"Očakávaný PK: {expected_primary_key}, ale je: {pk}"

def test_ambulance_foreign_keys():
    """Test na overenie CUDZÍCH kľúčov v tabuľke `ambulance`."""
    fks = get_foreign_keys("ambulance")
    for expected_fk in expected_foreign_keys:
        assert expected_fk in fks, f"Chýba FK: {expected_fk}, nájdené: {fks}"