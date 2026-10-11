import os
import uuid
import shutil
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, delete

from app.api.deps import get_db
from app.config import settings
from app.models.contract import Contract
from app.models.audit import AuditLog
from app.schemas.contract_schemas import (
    ContractSummaryResponse,
    ContractDetailResponse,
    ContractCompareRequest,
    ContractCompareResponse,
    SectionDiffItem,
)
from app.services.pdf_processor import pdf_processor
from app.services.rag_engine import rag_engine
from app.services.diff_engine import diff_engine
from app.agents.graph import contract_graph
from app.agents.state import ContractReviewState

router = APIRouter()

SAMPLE_BENCHMARKS = {
    "ma": {
        "title": "Cross-Border Tech M&A Agreement",
        "file": "cross_border_ma.txt",
        "playbook": "Strict Enterprise Playbook",
    },
    "cross_border_ma": {
        "title": "Cross-Border Tech M&A Agreement",
        "file": "cross_border_ma.txt",
        "playbook": "Strict Enterprise Playbook",
    },
    "cloud_dpa": {
        "title": "Enterprise Cloud & AI Data Processing Agreement",
        "file": "cloud_ai_dpa.txt",
        "playbook": "Standard Corporate Playbook",
    },
    "cloud_ai_dpa": {
        "title": "Enterprise Cloud & AI Data Processing Agreement",
        "file": "cloud_ai_dpa.txt",
        "playbook": "Standard Corporate Playbook",
    },
    "joint_ip": {
        "title": "Autonomous AI Joint R&D & IP License",
        "file": "ai_joint_rd.txt",
        "playbook": "Strict Enterprise Playbook",
    },
    "ai_joint_rd": {
        "title": "Autonomous AI Joint R&D & IP License",
        "file": "ai_joint_rd.txt",
        "playbook": "Strict Enterprise Playbook",
    },
    "msa": {
        "title": "Master Services Agreement (MSA)",
        "file": "enterprise_msa.txt",
        "playbook": "Standard Corporate Playbook",
    },
    "enterprise_msa": {
        "title": "Master Services Agreement (MSA)",
        "file": "enterprise_msa.txt",
        "playbook": "Standard Corporate Playbook",
    },
    "saas": {
        "title": "Enterprise SaaS Subscription Agreement",
        "file": "saas_agreement.txt",
        "playbook": "Balanced Commercial Playbook",
    },
    "saas_agreement": {
        "title": "Enterprise SaaS Subscription Agreement",
        "file": "saas_agreement.txt",
        "playbook": "Balanced Commercial Playbook",
    },
    "nda": {
        "title": "Mutual Non-Disclosure Agreement",
        "file": "mutual_nda.txt",
        "playbook": "Founder Friendly Playbook",
    },
    "mutual_nda": {
        "title": "Mutual Non-Disclosure Agreement",
        "file": "mutual_nda.txt",
        "playbook": "Founder Friendly Playbook",
    },
}


MAX_UPLOAD_BYTES = 25 * 1024 * 1024  # 25 MB


@router.post("/upload", response_model=ContractDetailResponse)
async def upload_contract(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    playbook_name: Optional[str] = Form("Standard Corporate Playbook"),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload contract PDF or TXT, extract text & tables via PyMuPDF,
    run PII redaction, index into RAG/ChromaDB, and create contract record.
    Enforces file size limit (25MB) and supported mime formats.
    """
    filename = file.filename or "contract.pdf"
    lower_name = filename.lower()
    if not (lower_name.endswith(".pdf") or lower_name.endswith(".txt") or lower_name.endswith(".docx")):
        raise HTTPException(status_code=400, detail="Only PDF, TXT, or DOCX contract files are supported")

    contract_id = str(uuid.uuid4())
    clean_filename = f"{contract_id[:8]}_{filename}"
    save_path = settings.UPLOAD_DIR / clean_filename

    # Read bytes and validate size
    try:
        content_bytes = await file.read()
        if len(content_bytes) > MAX_UPLOAD_BYTES:
            raise HTTPException(status_code=413, detail=f"File exceeds maximum upload size of 25MB")

        with open(save_path, "wb") as buffer:
            buffer.write(content_bytes)

        # Process PDF and extract text & sections
        raw_text, sections = pdf_processor.extract_from_pdf(str(save_path))
        doc_title = title or Path(filename).stem.replace("_", " ").title()

        # Index into RAG Engine / ChromaDB
        rag_engine.chunk_contract(contract_id, doc_title, sections)

        contract = Contract(
            id=contract_id,
            title=doc_title,
            original_filename=filename,
            file_path=str(save_path),
            status="uploaded",
            overall_risk_score=0.0,
            raw_text=raw_text,
            playbook_name=playbook_name,
            extracted_sections=sections,
            identified_risks=[],
            debate_transcript=[],
            redlines=[],
            obligations=[],
            risk_summary={"critical": 0, "high": 0, "medium": 0, "low": 0},
        )

        db.add(contract)
        await db.commit()
        await db.refresh(contract)
        return contract
    except HTTPException:
        if save_path.exists():
            save_path.unlink(missing_ok=True)
        raise
    except Exception as e:
        if save_path.exists():
            save_path.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail=f"Failed to process contract upload: {str(e)}")


@router.post("/demo/{sample_type}", response_model=ContractDetailResponse)
async def load_demo_contract(
    sample_type: str,
    llm_provider: Optional[str] = Query("gemini"),
    model_name: Optional[str] = Query("gemini-2.0-flash"),
    playbook: Optional[str] = Query(None),
    use_local_llm: bool = Query(False),
    db: AsyncSession = Depends(get_db),
):
    """
    Instant load and auto-analyze benchmark contract.
    Executes the 4-agent stategraph pipeline immediately.
    """
    sample_key = sample_type.lower()
    if sample_key not in SAMPLE_BENCHMARKS:
        raise HTTPException(
            status_code=404,
            detail=f"Benchmark '{sample_type}' not found. Available: {list(SAMPLE_BENCHMARKS.keys())}",
        )

    meta = SAMPLE_BENCHMARKS[sample_key]
    sample_file = settings.BASE_DIR.parent / "sample_contracts" / meta["file"]

    if sample_file.exists():
        raw_content = sample_file.read_text(encoding="utf-8", errors="ignore")
    else:
        raw_content = f"SECTION 1. GENERAL PROVISIONS\nStandard legal terms for {meta['title']}."

    contract_id = str(uuid.uuid4())
    sections = pdf_processor.segment_sections(raw_content)

    # Chunk into RAG
    rag_engine.chunk_contract(contract_id, meta["title"], sections)

    selected_playbook = playbook or meta["playbook"]

    contract = Contract(
        id=contract_id,
        title=meta["title"],
        original_filename=meta["file"],
        file_path=str(sample_file),
        status="processing",
        overall_risk_score=0.0,
        raw_text=raw_content,
        playbook_name=selected_playbook,
        extracted_sections=sections,
        identified_risks=[],
        debate_transcript=[],
        redlines=[],
        obligations=[],
        risk_summary={"critical": 0, "high": 0, "medium": 0, "low": 0},
    )
    db.add(contract)
    await db.commit()
    await db.refresh(contract)

    # Immediately execute agent graph
    state: ContractReviewState = {
        "contract_id": contract_id,
        "contract_title": meta["title"],
        "raw_text": raw_content,
        "sections": sections,
        "playbook_rules": [],
        "debate_cycle": 1,
        "max_debate_cycles": 1,
        "use_local_llm": use_local_llm,
        "llm_provider": llm_provider,
        "model_name": model_name,
        "api_key_override": None,
        "identified_risks": [],
        "debate_transcript": [],
        "redlines": [],
        "obligations": [],
        "risk_summary": {"critical": 0, "high": 0, "medium": 0, "low": 0},
        "overall_score": 0.0,
        "current_status": "processing",
        "error": None,
    }

    final_state = await contract_graph.execute(state)

    # Reload from DB
    db.expire_all()
    stmt = select(Contract).where(Contract.id == contract_id)
    res = await db.execute(stmt)
    updated_contract = res.scalar_one()
    return updated_contract


@router.get("/", response_model=List[ContractSummaryResponse])
async def list_contracts(
    skip: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(50, ge=1, le=100, description="Limit items per page"),
    db: AsyncSession = Depends(get_db),
):
    """List all contracts ordered by created_at DESC with pagination."""
    stmt = select(Contract).order_by(desc(Contract.created_at)).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("/compare", response_model=ContractCompareResponse)
async def compare_contracts(
    body: ContractCompareRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Side-by-side legal comparison between two contracts.
    Identifies added, removed, and modified sections, computes token diffs, and risk score delta.
    """
    stmt_base = select(Contract).where(Contract.id == body.base_contract_id)
    res_base = await db.execute(stmt_base)
    base_c = res_base.scalar_one_or_none()
    if not base_c:
        raise HTTPException(status_code=404, detail=f"Base contract '{body.base_contract_id}' not found")

    stmt_tgt = select(Contract).where(Contract.id == body.target_contract_id)
    res_tgt = await db.execute(stmt_tgt)
    tgt_c = res_tgt.scalar_one_or_none()
    if not tgt_c:
        raise HTTPException(status_code=404, detail=f"Target contract '{body.target_contract_id}' not found")

    base_secs = {s.get("title", f"Section {i}"): s.get("content", "") for i, s in enumerate(base_c.extracted_sections or [])}
    tgt_secs = {s.get("title", f"Section {i}"): s.get("content", "") for i, s in enumerate(tgt_c.extracted_sections or [])}

    all_titles = list(dict.fromkeys(list(base_secs.keys()) + list(tgt_secs.keys())))
    diff_items = []

    for title in all_titles:
        b_text = base_secs.get(title)
        t_text = tgt_secs.get(title)

        if b_text is not None and t_text is not None:
            if b_text.strip() == t_text.strip():
                diff_items.append(SectionDiffItem(
                    section_title=title,
                    status="identical",
                    diff_tokens=[{"type": "equal", "text": b_text[:200]}],
                ))
            else:
                tokens = diff_engine.generate_clause_diff(b_text, t_text)
                diff_items.append(SectionDiffItem(
                    section_title=title,
                    status="modified",
                    diff_tokens=tokens,
                ))
        elif b_text is not None and t_text is None:
            diff_items.append(SectionDiffItem(
                section_title=title,
                status="removed",
                diff_tokens=[{"type": "delete", "text": b_text}],
            ))
        else:
            diff_items.append(SectionDiffItem(
                section_title=title,
                status="added",
                diff_tokens=[{"type": "insert", "text": t_text or ""}],
            ))

    risk_delta = round((tgt_c.overall_risk_score or 0.0) - (base_c.overall_risk_score or 0.0), 2)

    return ContractCompareResponse(
        base_id=base_c.id,
        base_title=base_c.title,
        target_id=tgt_c.id,
        target_title=tgt_c.title,
        base_risk_score=base_c.overall_risk_score or 0.0,
        target_risk_score=tgt_c.overall_risk_score or 0.0,
        risk_score_delta=risk_delta,
        sections=diff_items,
        source_id=base_c.id,
        source_title=base_c.title,
        source_risk_score=base_c.overall_risk_score or 0.0,
        risk_delta=risk_delta,
    )


@router.get("/{id}", response_model=ContractDetailResponse)
async def get_contract(id: str, db: AsyncSession = Depends(get_db)):
    """Fetch full contract details with risks, transcripts, redlines, and obligations."""
    stmt = select(Contract).where(Contract.id == id)
    res = await db.execute(stmt)
    contract = res.scalar_one_or_none()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract


@router.delete("/{id}")
async def delete_contract(id: str, db: AsyncSession = Depends(get_db)):
    """Delete contract, purge associated audit logs, file on disk, and clear ChromaDB vector collections."""
    stmt = select(Contract).where(Contract.id == id)
    res = await db.execute(stmt)
    contract = res.scalar_one_or_none()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    # 1. Purge from RAG / ChromaDB
    rag_engine.delete_contract(id)

    # 2. Delete file on disk if exists
    if contract.file_path:
        try:
            p = Path(contract.file_path)
            if p.exists() and "sample_contracts" not in str(p):
                p.unlink(missing_ok=True)
        except Exception:
            pass

    # 3. Delete database record (cascades to audit logs)
    await db.delete(contract)
    await db.commit()

    return {"status": "success", "message": f"Contract {id} deleted successfully"}
