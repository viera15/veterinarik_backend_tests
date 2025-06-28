import pymysql
import pytest
from config.db_config import DB_CONFIG

expected_tables = {
    "ambulance",
    "ambulance_asoc",
    "animals",
    "owner",
    "reception",
    "records",
    "templates",
    "testing",
    "token",
    "user"
}

def fetch_existing_tables():
    """
    Testovacia funkcia na získanie existujúcich tabuliek v databáze.
    Používa sa na porovnanie s očakávanými tabuľkami.
    Vráti množinu názvov tabuliek.
    V prípade, že sa nepodarí pripojiť k databáze, vyvolá výnimku.
    """
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES;")
            result = {row[0] for row in cursor.fetchall()}
        return result
    finally:
        conn.close()

def test_database_tables_exist():
    """
    Test na overenie existencie očakávaných tabuliek v databáze.
    V prípade, že niektorá tabuľka chýba, test zlyhá a vypíše chýbajúce tabuľky.
    """
    existing_tables = fetch_existing_tables()
    missing = expected_tables - existing_tables
    assert not missing, f"Chýbajúce tabuľky v DB: {missing}"