import os
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.config import settings
from app.database import get_db
from app.models.contract import Contract
from app.schemas.contract_schemas import ContractUploadResponse, ContractListItem, ContractDetailResponse
from app.services.pdf_processor import pdf_processor
from app.services.rag_engine import rag_engine
from app.agents.graph import orchestrator

router = APIRouter(prefix="/contracts", tags=["Contracts"])


@router.post("/upload", response_model=ContractUploadResponse)
async def upload_contract(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    playbook_name: str = Form("Standard Corporate Playbook"),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload and parse raw contract PDF.
    Extracts native text, segments sections, and indexes contextual RAG chunks.
    """
    filename = file.filename or "contract.pdf"
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    contract_id = str(uuid.uuid4())
    clean_filename = f"{contract_id}_{filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, clean_filename)

    # Save uploaded file to disk
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    contract_title = title if title and title.strip() else file.filename.rsplit(".", 1)[0]

    try:
        # Extract text & sections using hybrid PDF processor
        raw_text, sections = pdf_processor.extract_text_and_sections(file_path)

        # Index contextual chunks into ChromaDB
        rag_engine.index_contract(
            contract_id=contract_id,
            contract_title=contract_title,
            sections=sections
        )

        # Create Contract record
        contract = Contract(
            id=contract_id,
            title=contract_title,
            original_filename=file.filename,
            file_path=file_path,
            status="uploaded",
            raw_text=raw_text,
            playbook_name=playbook_name,
            extracted_sections=sections
        )
        db.add(contract)
        await db.commit()
        await db.refresh(contract)

        return ContractUploadResponse(
            id=contract.id,
            title=contract.title,
            original_filename=contract.original_filename,
            status=contract.status,
            message="Contract uploaded, parsed, and indexed successfully.",
            created_at=contract.created_at
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error parsing contract PDF: {str(e)}"
        )


@router.post("/demo/{sample_type}")
async def load_demo_contract(
    sample_type: str,
    llm_provider: Optional[str] = None,
    model_name: Optional[str] = None,
    playbook: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Instant one-click loading and multi-agent analysis of benchmark test contracts."""
    sample_map = {
        "msa": ("Sample_Enterprise_MSA.pdf", "Enterprise Master Services Agreement", "Standard Corporate Playbook"),
        "saas": ("Sample_SaaS_Vendor_Agreement.pdf", "Cloud SaaS Subscription Agreement", "Vendor Friendly Playbook"),
        "nda": ("Sample_Mutual_NDA.pdf", "Mutual Non-Disclosure Agreement", "Standard Corporate Playbook"),
        "ma": ("Complex_CrossBorder_MA_AssetPurchase.pdf", "Cross-Border Tech M&A & Asset Purchase Agreement", "Strict Compliance Playbook"),
        "cloud_dpa": ("Complex_Enterprise_Cloud_DPA_SLA.pdf", "Global Enterprise Cloud & AI Infrastructure MSA (DPA/SLA)", "Vendor Friendly Playbook"),
        "joint_ip": ("Complex_JointDevelopment_IP_Licensing.pdf", "Strategic AI Joint Development & Cross-Licensing Agreement", "Standard Corporate Playbook")
    }

    key = sample_type.lower()
    if key not in sample_map:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid sample type '{sample_type}'. Choose from: msa, saas, nda, ma, cloud_dpa, joint_ip."
        )

    filename, title, default_playbook = sample_map[key]
    playbook_name = playbook or default_playbook

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    candidates = [
        os.path.join(base_dir, "sample_contracts", filename),
        os.path.join(os.getcwd(), "sample_contracts", filename),
        os.path.join(os.getcwd(), "..", "sample_contracts", filename),
        os.path.join(os.path.dirname(os.getcwd()), "sample_contracts", filename),
        os.path.join(os.path.expanduser("~"), "Desktop", "ContractMind_Samples", filename),
    ]
    file_path = next((p for p in candidates if os.path.exists(p)), None)

    if not file_path:
        raise HTTPException(status_code=404, detail=f"Sample contract file '{filename}' not found.")

    contract_id = str(uuid.uuid4())
    raw_text, sections = pdf_processor.extract_text_and_sections(file_path)

    rag_engine.index_contract(
        contract_id=contract_id,
        contract_title=title,
        sections=sections
    )

    contract = Contract(
        id=contract_id,
        title=title,
        original_filename=filename,
        file_path=file_path,
        status="processing",
        raw_text=raw_text,
        playbook_name=playbook_name,
        extracted_sections=sections
    )
    db.add(contract)
    await db.commit()

    use_local = (llm_provider == "ollama")
    final_state = await orchestrator.run(
        contract_id=contract_id,
        contract_title=title,
        raw_text=raw_text,
        sections=sections,
        playbook_rules=[],
        use_local_llm=use_local,
        llm_provider=llm_provider,
        model_name=model_name,
        db=db
    )

    return {
        "id": contract_id,
        "title": title,
        "status": "analyzed",
        "overall_risk_score": final_state.get("overall_score", 0.0),
        "redlines_count": len(final_state.get("redlines", [])),
        "obligations_count": len(final_state.get("obligations", [])),
        "message": f"Successfully loaded and reviewed {title}"
    }


@router.get("/", response_model=List[ContractListItem])
async def list_contracts(db: AsyncSession = Depends(get_db)):
    """List all uploaded contracts."""
    stmt = select(Contract).order_by(desc(Contract.created_at))
    result = await db.execute(stmt)
    contracts = result.scalars().all()
    return contracts


@router.get("/{contract_id}", response_model=ContractDetailResponse)
async def get_contract(contract_id: str, db: AsyncSession = Depends(get_db)):
    """Retrieve full details, redlines, risks, and obligations for a contract."""
    stmt = select(Contract).where(Contract.id == contract_id)
    result = await db.execute(stmt)
    contract = result.scalars().first()

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    return ContractDetailResponse(
        id=contract.id,
        title=contract.title,
        original_filename=contract.original_filename,
        status=contract.status,
        error_message=contract.error_message,
        playbook_name=contract.playbook_name,
        overall_risk_score=contract.overall_risk_score,
        risk_summary=contract.risk_summary or {},
        redlines=contract.redlines or [],
        obligations=contract.obligations or [],
        debate_transcript=contract.debate_transcript or [],
        created_at=contract.created_at,
        updated_at=contract.updated_at
    )


@router.delete("/{contract_id}")
async def delete_contract(contract_id: str, db: AsyncSession = Depends(get_db)):
    """Delete a contract and associated records."""
    stmt = select(Contract).where(Contract.id == contract_id)
    result = await db.execute(stmt)
    contract = result.scalars().first()

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    if os.path.exists(contract.file_path):
        try:
            os.remove(contract.file_path)
        except Exception:
            pass

    rag_engine.delete_contract(contract_id)

    await db.delete(contract)
    await db.commit()
    return {"message": "Contract deleted successfully", "id": contract_id}
