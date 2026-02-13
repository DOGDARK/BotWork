import re
from config import ADMIN_IDS

USERNAME_RE = re.compile(r"^@[a-zA-Z0-9_]{1,32}$")

def valid_username(text: str) -> bool:
    return bool(USERNAME_RE.match(text))


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS
