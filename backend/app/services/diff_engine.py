import difflib
import uuid
from typing import List, Dict, Any


class DiffEngine:
    """Calculates unified word-level and sentence-level diffs for legal redlining."""

    @staticmethod
    def generate_clause_diff(
        section_number: str,
        original_text: str,
        suggested_text: str,
        severity: str,
        rationale: str
    ) -> Dict[str, Any]:
        """
        Creates a structured redline object with classification (INSERT, DELETE, REPLACE).
        """
        diff_id = f"redline_{uuid.uuid4().hex[:8]}"

        if not original_text.strip() and suggested_text.strip():
            diff_type = "INSERT"
        elif original_text.strip() and not suggested_text.strip():
            diff_type = "DELETE"
        else:
            diff_type = "REPLACE"

        # Generate word-level diff tokens for frontend rendering
        orig_words = original_text.split()
        sugg_words = suggested_text.split()
        matcher = difflib.SequenceMatcher(None, orig_words, sugg_words)

        diff_tokens = []
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                diff_tokens.append({"type": "equal", "text": " ".join(orig_words[i1:i2])})
            elif tag == 'delete':
                diff_tokens.append({"type": "delete", "text": " ".join(orig_words[i1:i2])})
            elif tag == 'insert':
                diff_tokens.append({"type": "insert", "text": " ".join(sugg_words[j1:j2])})
            elif tag == 'replace':
                diff_tokens.append({"type": "delete", "text": " ".join(orig_words[i1:i2])})
                diff_tokens.append({"type": "insert", "text": " ".join(sugg_words[j1:j2])})

        return {
            "id": diff_id,
            "section_number": section_number,
            "original_text": original_text,
            "suggested_text": suggested_text,
            "diff_type": diff_type,
            "risk_severity": severity,
            "legal_rationale": rationale,
            "diff_tokens": diff_tokens,
            "accepted": None
        }


diff_engine = DiffEngine()
