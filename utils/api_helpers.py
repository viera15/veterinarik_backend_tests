# utils/api_helpers.py

def extract_items(response_data, key="items"):
    """
    Vytiahne zo štruktúry odpovede buď priamo zoznam, alebo hľadá zoznam podľa kľúča.
    Ak vráti len jeden objekt, zabalí ho do zoznamu.
    """
    if isinstance(response_data, list):
        return response_data
    elif isinstance(response_data, dict):
        if key in response_data and isinstance(response_data[key], list):
            return response_data[key]
        for value in response_data.values():
            if isinstance(value, list):
                return value
            if isinstance(value, dict) and key in value:
                return value[key]
    elif isinstance(response_data, str):
        return []
    return []
