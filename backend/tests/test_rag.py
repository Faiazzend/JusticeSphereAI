import pytest
from app.services.rag_engine import rag_engine


def test_contextual_chunking():
    sections = [
        {
            "section_number": "4.1",
            "title": "Payment Obligations",
            "content": "Client shall pay invoices within Net 30 days of submission.",
            "page_number": 2
        }
    ]

    chunks = rag_engine.semantic_chunk_and_contextualize("Vendor Agreement", sections)
    assert len(chunks) == 1
    assert "Section: 4.1" in chunks[0]["text"]
    assert "Vendor Agreement" in chunks[0]["text"]
    assert chunks[0]["metadata"]["page_number"] == 2
