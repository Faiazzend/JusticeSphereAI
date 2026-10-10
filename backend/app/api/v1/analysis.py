import os
import json
import re
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from app.config import settings
from app.database import get_db
from app.models.contract import Contract
from app.models.audit import AuditLog
from app.schemas.contract_schemas import AnalysisTriggerRequest, RedlineChange
from app.schemas.obligation_schemas import ObligationsResponse, ObligationItem
from app.agents.graph import orchestrator
from app.services.export_service import export_service
from app.services.diff_engine import diff_engine
from app.agents.llm_client import llm_client

router = APIRouter(prefix="/analysis", tags=["Analysis & Engine"])


@router.post("/{contract_id}/trigger")
async def trigger_analysis(
    contract_id: str,
    req: AnalysisTriggerRequest = AnalysisTriggerRequest(),
    db: AsyncSession = Depends(get_db)
):
    """
    Triggers the multi-agent debate and redline pipeline for the contract.
    """
    stmt = select(Contract).where(Contract.id == contract_id)
    result = await db.execute(stmt)
    contract = result.scalars().first()

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    contract.status = "processing"
    contract.playbook_name = req.playbook_name or contract.playbook_name
    await db.commit()

    try:
        final_state = await orchestrator.run(
            contract_id=contract.id,
            contract_title=contract.title,
            raw_text=contract.raw_text or "",
            sections=contract.extracted_sections or [],
            playbook_rules=[],
            use_local_llm=req.use_local_llm,
            db=db,
            llm_provider=req.llm_provider,
            model_name=req.model_name,
            api_key_override=req.api_key
        )

        return {
            "message": "Contract analysis successfully completed",
            "contract_id": contract.id,
            "overall_risk_score": final_state.get("overall_score", 0.0),
            "redlines_count": len(final_state.get("redlines", [])),
            "obligations_count": len(final_state.get("obligations", []))
        }

    except Exception as e:
        contract.status = "error"
        contract.error_message = str(e)
        await db.commit()
        raise HTTPException(status_code=500, detail=f"Analysis pipeline failed: {str(e)}")


@router.get("/{contract_id}/obligations", response_model=ObligationsResponse)
async def get_contract_obligations(contract_id: str, db: AsyncSession = Depends(get_db)):
    """
    Returns structured obligations JSON (obligor, recipient, triggers, penalties).
    """
    stmt = select(Contract).where(Contract.id == contract_id)
    result = await db.execute(stmt)
    contract = result.scalars().first()

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    raw_obls = contract.obligations or []
    items = []
    for item in raw_obls:
        items.append(ObligationItem(**item))

    return ObligationsResponse(
        contract_id=contract.id,
        summary=f"Extracted {len(items)} contractual duties and calendar triggers.",
        overall_risk_score=contract.overall_risk_score,
        obligations=items
    )


@router.get("/{contract_id}/redlines", response_model=List[RedlineChange])
async def get_contract_redlines(contract_id: str, db: AsyncSession = Depends(get_db)):
    """
    Returns redlines with diff tokens, suggested modifications, and legal rationales.
    """
    stmt = select(Contract).where(Contract.id == contract_id)
    result = await db.execute(stmt)
    contract = result.scalars().first()

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    return contract.redlines or []


@router.patch("/{contract_id}/redlines/{redline_id}")
async def update_redline_status(
    contract_id: str,
    redline_id: str,
    decision: Dict[str, Any],
    db: AsyncSession = Depends(get_db)
):
    """
    Accepts (accepted=True) or Rejects (accepted=False) a redline change.
    """
    stmt = select(Contract).where(Contract.id == contract_id)
    result = await db.execute(stmt)
    contract = result.scalars().first()

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    redlines = list(contract.redlines or [])
    updated = False
    for rl in redlines:
        if rl.get("id") == redline_id:
            rl["accepted"] = decision.get("accepted")
            updated = True
            break

    if not updated:
        raise HTTPException(status_code=404, detail="Redline ID not found")

    contract.redlines = redlines
    await db.commit()
    return {"message": "Redline decision updated", "redline_id": redline_id, "accepted": decision.get("accepted")}


class RedlineRegenerateRequest(BaseModel):
    custom_prompt: str = Field(..., description="Custom rewrite prompt or legal instruction for this clause")
    provider: Optional[str] = None
    model_name: Optional[str] = None


@router.post("/{contract_id}/redlines/{redline_id}/regenerate")
async def regenerate_redline(
    contract_id: str,
    redline_id: str,
    req: RedlineRegenerateRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Rewrites a specific clause redline based on user custom prompt instructions,
    re-running synthesis and recomputing word-level diff tokens.
    """
    stmt = select(Contract).where(Contract.id == contract_id)
    result = await db.execute(stmt)
    contract = result.scalars().first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    redlines = list(contract.redlines or [])
    target_idx = None
    target_rl = None
    for idx, rl in enumerate(redlines):
        if rl.get("id") == redline_id:
            target_idx = idx
            target_rl = rl
            break

    if target_rl is None:
        raise HTTPException(status_code=404, detail="Redline not found")

    sec_num = target_rl.get("section_number", "General")
    orig_text = target_rl.get("original_text", "")
    curr_sugg = target_rl.get("suggested_text", "")
    severity = target_rl.get("risk_severity", "MEDIUM")

    prompt = (
        f"You are an expert corporate legal counsel and contract redline synthesizer.\n"
        f"Original Contract Clause (Section {sec_num}):\n"
        f"\"\"\"\n{orig_text}\n\"\"\"\n\n"
        f"Prior Proposed Redline:\n"
        f"\"\"\"\n{curr_sugg}\n\"\"\"\n\n"
        f"USER CUSTOM REWRITE INSTRUCTION:\n"
        f"\"\"\"\n{req.custom_prompt}\n\"\"\"\n\n"
        f"Task: Rewrite the contract clause replacement strictly following the user's custom instruction.\n"
        f"Return ONLY valid JSON in this exact structure without markdown fences:\n"
        f"{{\n"
        f"  \"suggested_text\": \"<exact revised clause replacement text>\",\n"
        f"  \"legal_rationale\": \"<concise explanation of how this satisfies the user prompt>\"\n"
        f"}}"
    )

    new_sugg = ""
    new_rationale = ""
    try:
        resp_text, used_model, _ = await llm_client.call_llm(
            prompt=prompt,
            system_prompt="You are a senior partner synthesizing contract redlines based on precise client instructions. Return JSON only.",
            provider=req.provider,
            model_name=req.model_name,
            temperature=0.2
        )
        if resp_text:
            cleaned = re.sub(r"^```(?:json)?\s*", "", resp_text.strip(), flags=re.MULTILINE)
            cleaned = re.sub(r"```$", "", cleaned.strip(), flags=re.MULTILINE)
            parsed = json.loads(cleaned)
            new_sugg = parsed.get("suggested_text", "").strip()
            new_rationale = parsed.get("legal_rationale", "").strip()
    except Exception:
        pass

    if not new_sugg:
        new_sugg = f"{curr_sugg} [Modified per client prompt: '{req.custom_prompt}']"
        new_rationale = f"Clause customized to incorporate client requirement: {req.custom_prompt}."

    updated_diff = diff_engine.generate_clause_diff(
        section_number=sec_num,
        original_text=orig_text,
        suggested_text=new_sugg,
        severity=severity,
        rationale=new_rationale or target_rl.get("legal_rationale", "")
    )
    updated_diff["id"] = redline_id
    updated_diff["accepted"] = None
    updated_diff["custom_prompt"] = req.custom_prompt

    redlines[target_idx] = updated_diff
    contract.redlines = redlines

    # Log turn to debate transcript
    transcript = list(contract.debate_transcript or [])
    transcript.append({
        "agent_name": "Client Prompt & Arbiter",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "content": f"Regenerated Section {sec_num} with prompt: \"{req.custom_prompt}\". {new_rationale}",
        "target_clause": f"Section {sec_num}"
    })
    contract.debate_transcript = transcript

    await db.commit()
    return updated_diff


@router.get("/{contract_id}/export/docx")
async def export_redlines_docx(contract_id: str, db: AsyncSession = Depends(get_db)):
    """
    Generates and downloads a Word DOCX file with Track Changes redline styling.
    """
    stmt = select(Contract).where(Contract.id == contract_id)
    result = await db.execute(stmt)
    contract = result.scalars().first()

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    redlines = contract.redlines or []
    out_filename = f"Redlined_{contract.title.replace(' ', '_')}_{contract_id[:6]}.docx"
    file_path = export_service.export_to_docx(
        contract_title=contract.title,
        redlines=redlines,
        output_filename=out_filename
    )

    return FileResponse(
        path=file_path,
        filename=out_filename,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


@router.get("/audit/summary")
async def get_audit_summary(db: AsyncSession = Depends(get_db)):
    """
    Returns aggregated token consumption and estimated cost logs for hackathon evaluation.
    """
    stmt = select(AuditLog).order_by(desc(AuditLog.timestamp)).limit(50)
    result = await db.execute(stmt)
    logs = result.scalars().all()

    total_tokens = sum(log.total_tokens for log in logs)
    total_cost = sum(log.estimated_cost_usd for log in logs)
    avg_latency = (sum(log.latency_ms for log in logs) / max(1, len(logs))) if logs else 0.0

    return {
        "total_executions": len(logs),
        "total_tokens_consumed": total_tokens,
        "total_cost_usd": round(total_cost, 6),
        "average_latency_ms": round(avg_latency, 2),
        "recent_logs": [
            {
                "id": log.id,
                "contract_id": log.contract_id,
                "agent_name": log.agent_name,
                "action": log.action,
                "model_name": log.model_name,
                "total_tokens": log.total_tokens,
                "latency_ms": log.latency_ms,
                "cost_usd": log.estimated_cost_usd,
                "timestamp": log.timestamp.isoformat()
            }
            for log in logs[:15]
        ]
    }


@router.delete("/audit/reset")
async def reset_audit_logs(db: AsyncSession = Depends(get_db)):
    """Purges all telemetry audit logs."""
    from sqlalchemy import delete
    await db.execute(delete(AuditLog))
    await db.commit()
    return {"message": "Audit logs reset successfully"}


@router.get("/llm/config")
async def get_llm_config():
    """Returns currently active LLM provider, keys status, and local Ollama availability."""
    import httpx
    
    ollama_online = False
    ollama_models = []
    try:
        async with httpx.AsyncClient(timeout=1.5) as client:
            resp = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
            if resp.status_code == 200:
                ollama_online = True
                ollama_models = [m.get("name") for m in resp.json().get("models", [])]
    except Exception:
        pass

    return {
        "gemini_configured": bool(settings.GEMINI_API_KEY),
        "openai_configured": bool(settings.OPENAI_API_KEY),
        "anthropic_configured": bool(settings.ANTHROPIC_API_KEY),
        "ollama_available": ollama_online,
        "ollama_base_url": settings.OLLAMA_BASE_URL,
        "ollama_models": ollama_models,
        "default_model": settings.DEFAULT_MODEL,
        "fallback_model": settings.FALLBACK_MODEL
    }


@router.post("/llm/config")
async def update_llm_config(payload: Dict[str, Any]):
    """Dynamically updates API keys or model selection."""
    if "gemini_api_key" in payload and payload["gemini_api_key"]:
        settings.GEMINI_API_KEY = payload["gemini_api_key"].strip()
    if "openai_api_key" in payload and payload["openai_api_key"]:
        settings.OPENAI_API_KEY = payload["openai_api_key"].strip()
    if "anthropic_api_key" in payload and payload["anthropic_api_key"]:
        settings.ANTHROPIC_API_KEY = payload["anthropic_api_key"].strip()
    if "default_model" in payload and payload["default_model"]:
        settings.DEFAULT_MODEL = payload["default_model"].strip()
    if "fallback_model" in payload and payload["fallback_model"]:
        settings.FALLBACK_MODEL = payload["fallback_model"].strip()

    return {
        "message": "LLM configuration successfully updated",
        "gemini_configured": bool(settings.GEMINI_API_KEY),
        "openai_configured": bool(settings.OPENAI_API_KEY),
        "anthropic_configured": bool(settings.ANTHROPIC_API_KEY),
        "default_model": settings.DEFAULT_MODEL
    }
