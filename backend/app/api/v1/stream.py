import asyncio
import json
import logging
from typing import AsyncGenerator
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_db
from app.database import AsyncSessionLocal
from app.models.contract import Contract
from app.agents.graph import event_broadcaster

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/{id}")
@router.get("/debate/{id}")
async def stream_analysis(id: str):
    """
    Stream live agent debate events via SSE with real-time queue subscription,
    backlog replay of debate turns, and keep-alive heartbeats.
    """
    async def event_generator() -> AsyncGenerator[str, None]:
        queue = event_broadcaster.subscribe(id)
        try:
            # 1. Initial connection ack
            yield f"data: {json.dumps({'event': 'connected', 'contract_id': id})}\n\n"

            # 2. Check current DB state
            async with AsyncSessionLocal() as db:
                stmt = select(Contract).where(Contract.id == id)
                res = await db.execute(stmt)
                contract = res.scalar_one_or_none()

            # If contract is already analyzed, replay transcript and complete immediately
            if contract and contract.status == "analyzed":
                transcript = contract.debate_transcript or []
                for entry in transcript:
                    yield f"data: {json.dumps({'event': 'agent_turn', 'agent': entry.get('agent_name'), 'content': entry.get('content', '')[:160], 'target_clause': entry.get('target_clause')})}\n\n"
                    await asyncio.sleep(0.05)
                yield f"data: {json.dumps({'event': 'completed', 'status': 'analyzed', 'contract_id': id})}\n\n"
                return

            # If currently processing or queued, listen to live broadcaster events
            timeout_seconds = 60.0
            elapsed = 0.0
            while elapsed < timeout_seconds:
                try:
                    event_data = await asyncio.wait_for(queue.get(), timeout=2.0)
                    yield f"data: {json.dumps(event_data)}\n\n"
                    if event_data.get("event") == "completed":
                        break
                except asyncio.TimeoutError:
                    elapsed += 2.0
                    # Check DB to see if status updated in background
                    async with AsyncSessionLocal() as db:
                        stmt = select(Contract).where(Contract.id == id)
                        res = await db.execute(stmt)
                        check_contract = res.scalar_one_or_none()
                        if check_contract and check_contract.status in ("analyzed", "error"):
                            yield f"data: {json.dumps({'event': 'completed', 'status': check_contract.status, 'contract_id': id})}\n\n"
                            break
                    # Send comment heartbeat to keep connection alive
                    yield ": ping\n\n"

        except asyncio.CancelledError:
            logger.info(f"SSE client disconnected from contract {id}")
        finally:
            event_broadcaster.unsubscribe(id, queue)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
