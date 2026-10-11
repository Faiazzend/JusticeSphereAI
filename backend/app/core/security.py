import hashlib
import secrets
import hmac
import time
from typing import Optional


def generate_api_key(prefix: str = "cm_") -> str:
    """Generate a secure random API key."""
    return f"{prefix}{secrets.token_urlsafe(32)}"


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent directory traversal."""
    keep_chars = ("-", "_", ".", " ")
    clean = "".join(c for c in filename if c.isalnum() or c in keep_chars).rstrip()
    return clean or "contract.pdf"


def get_password_hash(password: str) -> str:
    """Hash password using salted SHA-256."""
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return f"{salt}${hashed}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against salted hash."""
    if "$" not in hashed_password:
        return False
    salt, hashed = hashed_password.split("$", 1)
    expected = hashlib.sha256((salt + plain_password).encode("utf-8")).hexdigest()
    return hmac.compare_digest(expected, hashed)


def create_access_token(subject: str, expires_delta_sec: int = 86400) -> str:
    """Generate signed bearer access token."""
    payload = f"{subject}:{time.time() + expires_delta_sec}"
    token_sig = hmac.new(b"contractmind-secret-key-2026", payload.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{payload}:{token_sig}"


def decode_access_token(token: str) -> Optional[str]:
    """Verify and decode signed access token."""
    parts = token.split(":")
    if len(parts) != 3:
        return None
    subject, exp_str, sig = parts
    payload = f"{subject}:{exp_str}"
    expected_sig = hmac.new(b"contractmind-secret-key-2026", payload.encode("utf-8"), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(sig, expected_sig):
        return None
    try:
        if float(exp_str) < time.time():
            return None
    except ValueError:
        return None
    return subject
