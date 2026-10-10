import os
import pytest
from app.services.pdf_processor import pdf_processor


def test_segment_sections_heuristic():
    sample_text = (
        "MASTER SERVICES AGREEMENT\n\n"
        "SECTION 1. DEFINITIONS\n"
        "Herein are the agreed terms and definitions of the agreement.\n\n"
        "SECTION 2. INDEMNIFICATION\n"
        "Vendor shall indemnify Client against all claims and damages.\n\n"
        "SECTION 3. LIMITATION OF LIABILITY\n"
        "Aggregate liability shall be capped at twelve months fees.\n"
    )

    sections = pdf_processor._segment_sections(sample_text, [{"page": 1, "text": sample_text}])
    assert len(sections) >= 2
    section_titles = [s["title"].upper() for s in sections]
    assert any("DEFINITIONS" in t for t in section_titles)
    assert any("INDEMNIFICATION" in t for t in section_titles)
