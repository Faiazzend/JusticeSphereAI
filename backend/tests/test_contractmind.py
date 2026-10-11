import pytest
import asyncio
from pathlib import Path
from docx import Document

from app.core.pii_redactor import pii_redactor
from app.services.pdf_processor import pdf_processor
from app.services.rag_engine import rag_engine
from app.services.diff_engine import diff_engine
from app.services.export_service import export_service
from app.core.token_tracker import token_tracker
from app.mcp_server.server import mcp_server


def test_pii_redactor():
    sample_text = (
        "Customer SSN is 123-45-6789 and credit card is 4111-2222-3333-4444. "
        "Contact email is john.doe@enterprise.com and phone is +1 (555) 123-4567. "
        "Bank account 123456789012 and Tax ID 12-3456789."
    )
    redacted, stats = pii_redactor.redact(sample_text)

    assert "[REDACTED_SSN]" in redacted
    assert "[REDACTED_CREDIT_CARD]" in redacted
    assert "[REDACTED_EMAIL]" in redacted
    assert "[REDACTED_PHONE]" in redacted
    assert "[REDACTED_BANK_ACCOUNT]" in redacted
    assert "[REDACTED_TAX_ID]" in redacted
    assert stats["SSN"] == 1
    assert stats["CREDIT_CARD"] == 1
    assert stats["EMAIL"] == 1
    assert stats["BANK_ACCOUNT"] == 1
    assert stats["TAX_ID"] == 1


def test_pdf_processor_table_formatting():
    table_matrix = [
        ["Service Tier", "Uptime Target", "Monthly Credit"],
        ["Tier 1", "99.9%", "10%"],
        ["Tier 2", "99.0%", "25%"],
    ]
    md_table = pdf_processor._format_markdown_table(table_matrix, page_num=1)
    assert "[TABLE EXHIBIT - Page 1]" in md_table
    assert "| Service Tier | Uptime Target | Monthly Credit |" in md_table
    assert "| Tier 1 | 99.9% | 10% |" in md_table


def test_diff_engine_tokens():
    orig = "Provider shall provide thirty (30) days notice."
    rev = "Provider shall provide sixty (60) days prior written notice."
    diff_tokens = diff_engine.generate_clause_diff(orig, rev)

    assert len(diff_tokens) > 0
    token_types = {t["type"] for t in diff_tokens}
    assert "equal" in token_types
    assert "delete" in token_types or "insert" in token_types


def test_docx_export_track_changes():
    redlines = [
        {
            "clause_id": "Section 2.1",
            "category": "Indemnification & Baskets",
            "diff_tokens": [
                {"type": "equal", "text": "Seller agrees to "},
                {"type": "delete", "text": "first-dollar tipping indemnity"},
                {"type": "insert", "text": "a true deductible basket capped at 1.0x fees"},
            ],
            "legal_rationale": "Mitigates uncapped liability.",
            "consensus_score": 25.0,
        }
    ]

    out_file = export_service.generate_docx_redline(
        contract_title="Test M&A Agreement",
        contract_id="test-uuid-1234",
        overall_risk_score=78.5,
        risk_summary={"critical": 1, "high": 1, "medium": 0, "low": 0},
        redlines=redlines,
        obligations=[
            {
                "obligation_type": "Notice",
                "obligor": "Seller",
                "recipient": "Buyer",
                "due_date_or_trigger": "24 hours",
                "penalty_for_breach": "Termination",
            }
        ],
    )

    assert Path(out_file).exists()

    # Verify that the generated file contains genuine OpenXML w:ins and w:del tags
    doc = Document(out_file)
    xml_content = doc._element.xml
    assert "w:del" in xml_content
    assert "w:ins" in xml_content
    assert "ContractMind Legal AI" in xml_content


def test_token_tracker_pricing():
    # Gemini
    cost_gemini = token_tracker.calculate_cost(1000, 1000, "gemini-3.5-flash-lite")
    assert cost_gemini == 0.000375

    # GPT-4o
    cost_openai = token_tracker.calculate_cost(1000, 1000, "gpt-4o")
    assert cost_openai == 0.02

    # Claude 3.5 Sonnet
    cost_claude = token_tracker.calculate_cost(1000, 1000, "claude-3-5-sonnet")
    assert cost_claude == 0.018

    # Ollama is 0
    cost_ollama = token_tracker.calculate_cost(1000, 1000, "ollama")
    assert cost_ollama == 0.0


def test_mcp_server_tools():
    tools = mcp_server.list_tools()
    tool_names = [t["name"] for t in tools]
    assert "evaluate_clause" in tool_names
    assert "get_playbook_rules" in tool_names
    assert "calculate_risk_matrix" in tool_names

    # Test evaluate_clause
    eval_res = mcp_server.call_tool(
        "evaluate_clause",
        {
            "clause_text": "Customer grants right to ingest data and train foundational models.",
            "clause_type": "ai_training",
        },
    )
    assert eval_res["is_compliant"] is False
    assert eval_res["risk_level"] == "CRITICAL"

    # Test calculate_risk_matrix
    matrix_res = mcp_server.call_tool(
        "calculate_risk_matrix",
        {"flagged_counts": {"critical": 2, "high": 1, "medium": 1}},
    )
    assert matrix_res["composite_score"] == 100.0
    assert matrix_res["governance_verdict"] == "REJECT / REDLINE"


def test_rag_engine_lifecycle():
    contract_id = "test-rag-999"
    sections = [
        {
            "section_number": "1",
            "title": "Confidentiality",
            "content": "Receiving Party shall preserve all confidential information without unauthorized disclosure.",
            "page_number": 1,
        }
    ]
    chunks = rag_engine.chunk_contract(contract_id, "Test Title", sections)
    assert len(chunks) >= 1
    assert "Context: This excerpt defines terms" in chunks[0]["text"]

    query_res = rag_engine.query(contract_id, "confidential disclosure", n_results=1)
    assert len(query_res) == 1

    rag_engine.delete_contract(contract_id)
    assert contract_id not in rag_engine._memory_store
