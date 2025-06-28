import pytest
from utils.db_helpers import (
    get_columns_metadata,
    get_foreign_keys,
    get_primary_key,
)

# Očakávané stĺpce a ich typy (z reálnej DB podľa screenshotu)
expected_columns = {
    "id": "int",
    "owner_id": "int",
    "vet_id": "int",
    "ambulance_id": "int",
    "born": "datetime",
    "died": "datetime",
    "name": "varchar",
    "spieces": "varchar",
    "description": "text",
    "chip": "varchar",
    "status": "int"
}

expected_not_nullable = {
    "id", "owner_id", "vet_id", "ambulance_id", "name", "spieces", "chip", "status"
}

expected_primary_key = "id"
expected_foreign_keys = {
    ("owner_id", "owner", "id"),
    ("ambulance_id", "ambulance", "id"),
}

def test_animals_columns_exist_and_types():
    """Test na overenie existencie očakávaných stĺpcov a ich typov v tabuľke `animals`."""
    cols = {col[0]: col[1] for col in get_columns_metadata("animals")}
    for col_name, expected_type in expected_columns.items():
        assert col_name in cols, f"Chýba stĺpec: {col_name}"
        assert expected_type in cols[col_name], f"Typ stĺpca {col_name} má byť {expected_type}, ale je {cols[col_name]}"

def test_animals_column_nullability():
    """Test na overenie nullovateľnosti (stĺpec nesmie byť prázdny) očakávaných stĺpcov v tabuľke `animals`."""
    cols = {col[0]: col[2] for col in get_columns_metadata("animals")}
    for col in expected_not_nullable:
        assert cols.get(col) == "NO", f"Stĺpec {col} by mal byť NOT NULL"

def test_animals_primary_key():
    """Test na overenie primárneho kľúča tabuľky `animals`."""
    pk = get_primary_key("animals")
    assert pk == expected_primary_key, f"Očakávaný PK: {expected_primary_key}, ale je: {pk}"

def test_animals_foreign_keys():
    """Test na overenie cudzích kľúčov v tabuľke `animals`."""
    fks = get_foreign_keys("animals")
    for expected_fk in expected_foreign_keys:
        assert expected_fk in fks, f"Chýba FK: {expected_fk}, nájdené: {fks}"