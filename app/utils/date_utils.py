from datetime import datetime

def parse_event_date(date_str):
    """
    Accepte :
    - YYYY-MM-DD
    - DD/MM/YYYY
    Retourne datetime ou None
    """
    if not date_str:
        return None

    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass

    return None
