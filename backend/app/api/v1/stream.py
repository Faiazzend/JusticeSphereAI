import asyncio
import json
from typing import AsyncGenerator
from fastapi import APIRouter, Depends, HTTPException
from sse_starlette.sse import EventSourceResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.contract import Contract

router = APIRouter(prefix="/stream", tags=["Streaming & Events"])


async def event_generator(contract_id: str, db: AsyncSession) -> AsyncGenerator[str, None]:
    """Generates real-time SSE stream of agent debate and review progress."""
    stmt = select(Contract).where(Contract.id == contract_id)
    result = await db.execute(stmt)
    contract = result.scalars().first()

    if not contract:
        yield json.dumps({"event": "error", "message": "Contract not found"})
        return

    # Initial ping
    yield json.dumps({
        "event": "connected",
        "contract_id": contract.id,
        "status": contract.status
    })

    # If already analyzed, stream the transcript turns smoothly
    turns = contract.debate_transcript or []
    if turns:
        for idx, turn in enumerate(turns):
            await asyncio.sleep(0.5)  # Realistic pacing for UI observation
            yield json.dumps({
                "event": "agent_turn",
                "index": idx + 1,
                "agent_name": turn.get("agent_name"),
                "timestamp": turn.get("timestamp"),
                "content": turn.get("content"),
                "target_clause": turn.get("target_clause")
            })

        yield json.dumps({
            "event": "completed",
            "overall_score": contract.overall_risk_score,
            "status": "analyzed"
        })
    else:
        # Awaiting processing
        yield json.dumps({
            "event": "waiting",
            "message": "Contract is queued or pending analysis trigger."
        })


@router.get("/{contract_id}")
async def stream_contract_debate(contract_id: str, db: AsyncSession = Depends(get_db)):
    """
    Server-Sent Events (SSE) endpoint delivering real-time agent debate messages.
    """
    return EventSourceResponse(event_generator(contract_id, db))
