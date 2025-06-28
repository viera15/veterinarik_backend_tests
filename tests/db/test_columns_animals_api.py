import pymysql
import pytest
from config.db_config import DB_CONFIG

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

def get_columns_metadata():

    """ Pomocná funkcia na získanie metadát stĺpcov tabuľky `animals`.
    Vráti zoznam stĺpcov s ich názvami, typmi a nullovateľnosťou.
    V prípade, že sa nepodarí pripojiť k databáze, vyvolá výnimku.
    """

    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SHOW COLUMNS FROM animals;")
            return cursor.fetchall()
    finally:
        conn.close()

def get_foreign_keys():

    """ Pomocná funkcia na získanie CUDZÍCH kľúčov tabuľky `animals`.
    Vráti množinu cudzích kľúčov vo forme (stĺpec, odkazovaná_tabulka, odkazovaný_stĺpec).
    V prípade, že sa nepodarí pripojiť k databáze, vyvolá výnimku.
    """

    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
                FROM information_schema.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'animals'
                AND REFERENCED_TABLE_NAME IS NOT NULL;
            """, (DB_CONFIG["database"],))
            return set(cursor.fetchall())
    finally:
        conn.close()

def get_primary_key():

    """ Pomocná funkcia na ZÍSKANIE primárneho kľúča tabuľky `animals`.
    Vráti názov primárneho kľúca.
    V prípade, že sa nepodarí pripojiť k databáze, vyvolá výnimku.
    """

    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SHOW KEYS FROM animals WHERE Key_name = 'PRIMARY';")
            result = cursor.fetchone()
            return result[4] if result else None
    finally:
        conn.close()

def test_animals_columns_exist_and_types():

    """ 
    Test na overenie existencie očakávaných stĺpcov a ich typov v tabuľke `animals`.        
    """

    cols = {col[0]: col[1] for col in get_columns_metadata()}
    for col_name, expected_type in expected_columns.items():
        assert col_name in cols, f"Chýba stĺpec: {col_name}"
        assert expected_type in cols[col_name], f"Typ stĺpca {col_name} má byť {expected_type}, ale je {cols[col_name]}"

def test_animals_column_nullability():

    """ 
    Test na overenie nullovateľnosti (stĺpec nesmie byť prázdny) očakávaných stĺpcov v tabuľke `animals`.        
    """

    cols = {col[0]: col[2] for col in get_columns_metadata()}
    for col in expected_not_nullable:
        assert cols.get(col) == "NO", f"Stĺpec {col} by mal byť NOT NULL"

def test_animals_primary_key():

    """ 
    Test na OVERENIE primárneho kľúca očakávaných stĺpcov v tabuľke `animals`.        
    """

    pk = get_primary_key()
    assert pk == expected_primary_key, f"Očakávaný PK: {expected_primary_key}, ale je: {pk}"

def test_animals_foreign_keys():

    """ 
    Test na overenie CUDZÍCH kľúcov očakávaných stĺpcov v tabuľke `animals`.        
    """

    fks = get_foreign_keys()
    for expected_fk in expected_foreign_keys:
        assert expected_fk in fks, f"Chýba FK: {expected_fk}, nájdené: {fks}"