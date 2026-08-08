import secrets
import string
from datetime import datetime, timedelta, timezone

BASE62_CHARACTERS: str = string.ascii_letters + string.digits

def generate_random_code(length : int = 6) -> str:
    return "".join(secrets.choice(BASE62_CHARACTERS) for _ in range(length))

def calculate_expiration_date(expire_in_days : int | None)->datetime| None:
    if expire_in_days is None:
        return None
    return datetime.now(timezone.utc) + timedelta(days= expire_in_days)
