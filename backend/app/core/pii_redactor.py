import re
from typing import Tuple, Dict


class PIIRedactor:
    """Detects and redacts sensitive personally identifiable information (PII)."""

    PATTERNS = {
        "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
        "CREDIT_CARD": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
        "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "PHONE": r"\b(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})\b",
        "BANK_ACCOUNT": r"\b\d{8,17}\b",
        "TAX_ID": r"\b\d{2}-\d{7}\b"
    }

    @classmethod
    def redact(cls, text: str) -> Tuple[str, Dict[str, int]]:
        """
        Redact sensitive information from text.
        Returns the sanitized text and a breakdown of redactions made.
        """
        if not text:
            return "", {}

        sanitized = text
        stats = {}

        for pii_type, pattern in cls.PATTERNS.items():
            matches = re.findall(pattern, sanitized)
            if matches:
                stats[pii_type] = len(matches)
                sanitized = re.sub(pattern, f"[REDACTED_{pii_type}]", sanitized)

        return sanitized, stats


pii_redactor = PIIRedactor()
