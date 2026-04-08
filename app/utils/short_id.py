import string
import secrets

ALPHABET = string.ascii_letters + string.digits  # a-zA-Z0-9
DEFAULT_LENGTH = 6


def generate_short_id(length: int = DEFAULT_LENGTH) -> str:
    """Generate a secure random short ID."""
    return ''.join(secrets.choice(ALPHABET) for _ in range(length))
