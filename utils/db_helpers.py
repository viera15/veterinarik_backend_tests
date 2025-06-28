import pymysql
from config.db_config import DB_CONFIG

def get_columns_metadata(table_name: str):
    """Získa zoznam stĺpcov s typmi a nullovateľnosťou."""
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SHOW COLUMNS FROM {table_name};")
            return cursor.fetchall()
    finally:
        conn.close()

def get_foreign_keys(table_name: str):
    """Získa cudzie kľúče z tabuľky vo forme (stĺpec, cieľová_tabuľka, cieľový_stĺpec)."""
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
                FROM information_schema.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
                AND REFERENCED_TABLE_NAME IS NOT NULL;
            """, (DB_CONFIG["database"], table_name))
            return set(cursor.fetchall())
    finally:
        conn.close()

def get_primary_key(table_name: str):
    """Získa názov primárneho kľúča danej tabuľky."""
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SHOW KEYS FROM {table_name} WHERE Key_name = 'PRIMARY';")
            result = cursor.fetchone()
            return result[4] if result else None
    finally:
        conn.close()