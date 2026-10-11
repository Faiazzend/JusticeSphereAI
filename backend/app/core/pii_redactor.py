import re
from typing import Dict, Tuple


class PIIRedactor:
    def __init__(self):
        # Order matters: SSN, Credit Card, Bank Account, Tax ID before generic phone patterns
        self.patterns = {
            "SSN": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
            "CREDIT_CARD": re.compile(r"\b(?:\d{4}[-\s]?){3}\d{4}\b"),
            "EMAIL": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
            "TAX_ID": re.compile(r"\b\d{2}-\d{7}\b"),
            "BANK_ACCOUNT": re.compile(r"\b\d{8,17}\b"),
            "PHONE": re.compile(
                r"(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]+(\d{3})[-. ]*(\d{4})\b"
            ),
        }

    def redact(self, text: str) -> Tuple[str, Dict[str, int]]:
        if not text:
            return "", {k: 0 for k in self.patterns.keys()}

        redacted_text = text
        stats: Dict[str, int] = {}

        for pii_type, pattern in self.patterns.items():
            matches = list(pattern.finditer(redacted_text))
            stats[pii_type] = len(matches)
            if matches:
                redacted_text = pattern.sub(f"[REDACTED_{pii_type}]", redacted_text)

        return redacted_text, stats


# Global instance
pii_redactor = PIIRedactor()
