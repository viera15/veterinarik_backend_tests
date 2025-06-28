import pymysql
import pytest

DB_CONFIG = {
    "host": "zasx.aleron.sk",
    "port": 3306,
    "user": "tester_veterinarik",
    "password": "6y7u8i9o",
    "database": "test_veterinarik"
}

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
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES;")
            result = {row[0] for row in cursor.fetchall()}
        return result
    finally:
        conn.close()

def test_database_tables_exist():
    existing_tables = fetch_existing_tables()
    missing = expected_tables - existing_tables
    assert not missing, f"Chýbajúce tabuľky v DB: {missing}"
