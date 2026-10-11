import re
from pathlib import Path
from typing import List, Tuple, Dict, Any

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

from app.core.pii_redactor import pii_redactor


class PDFProcessor:
    def __init__(self):
        self.section_pattern = re.compile(
            r"(?:\n|^)(?:SECTION|ARTICLE|CLAUSE)?\s*(\d+(?:\.\d+)*|[IVXLCDM]+)[\.\:\-\s]+([A-Z][A-Za-z0-9\s\,\-\&\/\(\)]+)(?=\n)",
            re.MULTILINE,
        )

    def _format_markdown_table(self, table_matrix: List[List[Any]], page_num: int) -> str:
        """Convert a 2D matrix into a clean Markdown table exhibit."""
        if not table_matrix or not table_matrix[0]:
            return ""

        headers = [str(c or "").strip().replace("\n", " ") for c in table_matrix[0]]
        # Fill empty headers
        headers = [h if h else f"Col {i+1}" for i, h in enumerate(headers)]

        lines = [f"\n[TABLE EXHIBIT - Page {page_num}]"]
        lines.append("| " + " | ".join(headers) + " |")
        lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

        for row in table_matrix[1:]:
            cells = [str(c or "").strip().replace("\n", " ") for c in row]
            # Ensure cell count matches header count
            if len(cells) < len(headers):
                cells += [""] * (len(headers) - len(cells))
            lines.append("| " + " | ".join(cells[:len(headers)]) + " |")

        lines.append("\n")
        return "\n".join(lines)

    def extract_from_pdf(self, file_path: str) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Ingests PDF, extracts page text and tabular layouts, runs PII redaction,
        and parses into structured sections.
        """
        path = Path(file_path)
        full_text_parts = []
        page_offsets = []  # (start_char, page_num)

        # Handle non-PDF or fallback text files
        if path.suffix.lower() != ".pdf" or fitz is None:
            if path.exists():
                text = path.read_text(encoding="utf-8", errors="ignore")
            else:
                text = ""
            redacted_text, _ = pii_redactor.redact(text)
            sections = self.segment_sections(redacted_text)
            return redacted_text, sections

        doc = fitz.open(file_path)
        try:
            for page_idx in range(len(doc)):
                page = doc[page_idx]
                page_num = page_idx + 1

                # 1. Extract plain text
                page_text = page.get_text("text") or ""

                # 2. Extract tables
                table_md = ""
                try:
                    tabs = page.find_tables()
                    if tabs and tabs.tables:
                        for tab in tabs:
                            table_matrix = tab.extract()
                            if table_matrix:
                                table_md += self._format_markdown_table(table_matrix, page_num)
                except Exception:
                    pass

                combined_page_text = page_text
                if table_md:
                    combined_page_text += "\n" + table_md

                full_text_parts.append(combined_page_text)
        finally:
            doc.close()

        combined_document = "\n\n".join(full_text_parts)

        # 3. PII Redaction
        redacted_document, _ = pii_redactor.redact(combined_document)

        # 4. Section Segmentation
        sections = self.segment_sections(redacted_document)
        return redacted_document, sections

    def segment_sections(self, text: str) -> List[Dict[str, Any]]:
        """
        Segments contract text using numbered headers.
        Falls back to paragraph blocks if no structured headers are detected.
        """
        matches = list(self.section_pattern.finditer(text))
        sections: List[Dict[str, Any]] = []

        if matches:
            for i, match in enumerate(matches):
                sec_num = match.group(1).strip()
                title = match.group(2).strip()
                start_pos = match.end()

                end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(text)
                content = text[start_pos:end_pos].strip()

                sections.append({
                    "section_number": sec_num,
                    "title": title,
                    "content": content,
                    "page_number": max(1, text[:match.start()].count("\f") + 1)
                })
        else:
            # Fallback to paragraph chunks
            paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
            for idx, para in enumerate(paragraphs):
                # Try to extract the first line as title
                lines = para.split("\n", 1)
                title = lines[0][:80] if lines else f"Section {idx+1}"
                content = lines[1] if len(lines) > 1 else para
                sections.append({
                    "section_number": str(idx + 1),
                    "title": title,
                    "content": content,
                    "page_number": max(1, text[:text.find(para)].count("\f") + 1)
                })

        return sections


pdf_processor = PDFProcessor()
