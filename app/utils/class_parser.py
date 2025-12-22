import re

def extract_year_from_class(classe: str):
    """
    Extrait l'année depuis une classe.
    Exemples:
    - 1A -> 1
    - 4D -> 4
    - 6INFO -> 6
    - 3 -> 3
    """
    if not classe:
        return None

    match = re.match(r"(\d+)", classe.strip())
    if match:
        return match.group(1)

    return None
