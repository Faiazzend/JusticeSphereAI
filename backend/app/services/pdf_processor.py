import os
import re
try:
    import pymupdf as fitz
except ImportError:
    import fitz  # PyMuPDF fallback
from app.core.pii_redactor import pii_redactor


class PDFProcessor:
    """Hybrid PDF extractor supporting native text, layout segmentation, table parsing, and PII sanitization."""

    @staticmethod
    def extract_text_and_sections(file_path: str, redact_pii: bool = True) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Reads a PDF file, extracts raw text, detects sections, and parses tabular structures.
        Returns: (full_raw_text, list_of_sections)
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")

        doc = fitz.open(file_path)
        full_text_chunks = []
        page_texts = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text")
            
            # Check for tables using pymupdf tabula / find_tables if supported
            table_markdown = ""
            try:
                tables = page.find_tables()
                if tables and len(tables.tables) > 0:
                    for tbl in tables.tables:
                        df = tbl.extract()
                        if df:
                            # Format as markdown table
                            header = " | ".join(str(cell or "").strip() for cell in df[0])
                            separator = " | ".join(["---"] * len(df[0]))
                            rows = [" | ".join(str(cell or "").strip() for cell in row) for row in df[1:]]
                            table_markdown += f"\n\n[TABLE EXHIBIT - Page {page_num + 1}]\n| {header} |\n| {separator} |\n"
                            for r in rows:
                                table_markdown += f"| {r} |\n"
            except Exception:
                table_markdown = ""

            page_content = text + ("\n" + table_markdown if table_markdown else "")
            page_texts.append({"page": page_num + 1, "text": page_content})
            full_text_chunks.append(page_content)

        doc.close()
        full_text = "\n\n".join(full_text_chunks)

        # Sanitize sensitive PII (SSNs, credit cards, bank accounts)
        if redact_pii:
            full_text, _ = pii_redactor.redact(full_text)

        # Segment full text into semantic sections using regex
        sections = PDFProcessor._segment_sections(full_text, page_texts)
        return full_text, sections

    @staticmethod
    def _segment_sections(full_text: str, page_texts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Segments raw contract text into structured clause sections."""
        # Matches patterns like:
        # "1. Definitions", "SECTION 2. INDEMNIFICATION", "3.1 Payment Terms", "Article IV - Warranties"
        section_pattern = re.compile(
            r"(?:\n|^)(?:SECTION|ARTICLE|CLAUSE)?\s*(\d+(?:\.\d+)*|[IVXLCDM]+)[\.\:\-\s]+([A-Z][A-Za-z0-9\s\,\-\&\/\(\)]+)(?=\n)",
            re.IGNORECASE
        )

        matches = list(section_pattern.finditer(full_text))
        sections = []

        if not matches:
            # Fallback: Segment by double newlines or paragraph blocks
            paragraphs = [p.strip() for p in full_text.split("\n\n") if len(p.strip()) > 30]
            for idx, para in enumerate(paragraphs):
                sections.append({
                    "section_number": f"Para {idx + 1}",
                    "title": para[:40] + "...",
                    "content": para,
                    "page_number": 1
                })
            return sections

        for i, match in enumerate(matches):
            section_num = match.group(1).strip()
            title = match.group(2).strip()
            start_pos = match.end()
            end_pos = matches[i + 1].start() if (i + 1) < len(matches) else len(full_text)
            content = full_text[start_pos:end_pos].strip()

            # Estimate page number
            estimated_page = 1
            char_count = 0
            for pt in page_texts:
                char_count += len(pt["text"])
                if char_count >= match.start():
                    estimated_page = pt["page"]
                    break

            sections.append({
                "section_number": section_num,
                "title": title,
                "content": content,
                "page_number": estimated_page
            })

        return sections


pdf_processor = PDFProcessor()
