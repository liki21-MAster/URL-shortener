import string

# The alphabet: 0-9, a-z, A-Z (62 characters)
BASE62 = string.digits + string.ascii_lowercase + string.ascii_uppercase

def id_to_short(num: int) -> str:
    """Converts a database ID (100) to a short code (1C)."""
    if num == 0:
        return BASE62[0]
    code = []
    while num > 0:
        num, rem = divmod(num, 62)
        code.append(BASE62[rem])
    return "".join(reversed(code))

def short_to_id(code: str) -> int:
    """Converts a short code (1C) back to a database ID (100)."""
    num = 0
    for char in code:
        num = num * 62 + BASE62.index(char)
    return num