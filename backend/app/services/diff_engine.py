import re
import difflib
from typing import List, Dict, Any


class DiffEngine:
    @staticmethod
    def _tokenize(text: str) -> List[str]:
        """Split text into words and whitespace chunks to preserve formatting."""
        return re.findall(r"\S+|\s+", text)

    def generate_clause_diff(self, original_text: str, revised_text: str) -> List[Dict[str, str]]:
        """
        Uses difflib.SequenceMatcher over word tokens.
        Outputs an array of diff tokens:
        [{"type": "equal"|"delete"|"insert", "text": "..."}]
        """
        orig_tokens = self._tokenize(original_text)
        rev_tokens = self._tokenize(revised_text)

        matcher = difflib.SequenceMatcher(None, orig_tokens, rev_tokens)
        diff_tokens: List[Dict[str, str]] = []

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "equal":
                diff_tokens.append({
                    "type": "equal",
                    "text": "".join(orig_tokens[i1:i2])
                })
            elif tag == "delete":
                diff_tokens.append({
                    "type": "delete",
                    "text": "".join(orig_tokens[i1:i2])
                })
            elif tag == "insert":
                diff_tokens.append({
                    "type": "insert",
                    "text": "".join(rev_tokens[j1:j2])
                })
            elif tag == "replace":
                diff_tokens.append({
                    "type": "delete",
                    "text": "".join(orig_tokens[i1:i2])
                })
                diff_tokens.append({
                    "type": "insert",
                    "text": "".join(rev_tokens[j1:j2])
                })

        # Compact adjacent tokens of same type
        compacted: List[Dict[str, str]] = []
        for token in diff_tokens:
            if not token["text"]:
                continue
            if compacted and compacted[-1]["type"] == token["type"]:
                compacted[-1]["text"] += token["text"]
            else:
                compacted.append(token)

        return compacted


diff_engine = DiffEngine()
