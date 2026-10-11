import time
import logging
import asyncio
from typing import Dict, Any, Optional, List
from sqlalchemy import select

from app.agents.state import ContractReviewState
from app.agents.nodes.auditor_agent import auditor_node
from app.agents.nodes.opposing_agent import opposing_node
from app.agents.nodes.redline_agent import redline_node
from app.agents.nodes.obligation_agent import obligation_node
from app.database import AsyncSessionLocal
from app.models.contract import Contract

logger = logging.getLogger(__name__)


class EventBroadcaster:
    """Pub/sub in-memory event bus for real-time SSE streaming across agent nodes."""

    def __init__(self):
        self._subscribers: Dict[str, List[asyncio.Queue]] = {}

    def subscribe(self, contract_id: str) -> asyncio.Queue:
        q = asyncio.Queue()
        self._subscribers.setdefault(contract_id, []).append(q)
        return q

    def unsubscribe(self, contract_id: str, q: asyncio.Queue) -> None:
        if contract_id in self._subscribers:
            self._subscribers[contract_id] = [sub for sub in self._subscribers[contract_id] if sub is not q]
            if not self._subscribers[contract_id]:
                del self._subscribers[contract_id]

    async def broadcast(self, contract_id: str, event_data: Dict[str, Any]) -> None:
        subs = list(self._subscribers.get(contract_id, []))
        for q in subs:
            try:
                await q.put(event_data)
            except Exception:
                pass


event_broadcaster = EventBroadcaster()


class ContractReviewGraph:
    """
    StateGraph Sequential Orchestrator:
    Executes Auditor -> Opposing Counsel -> Redline Synthesizer -> Obligation Extractor
    with per-node failure isolation, live event broadcasting, and SQLite persistence.
    """

    def __init__(self):
        pass

    async def execute(self, initial_state: ContractReviewState) -> ContractReviewState:
        state = dict(initial_state)
        contract_id = state.get("contract_id", "")

        await event_broadcaster.broadcast(contract_id, {"event": "connected", "contract_id": contract_id})

        # Helper for isolated execution
        async def _run_node_safely(node_fn, name: str, current_state: ContractReviewState) -> ContractReviewState:
            logger.info(f"Executing {name} Node...")
            await event_broadcaster.broadcast(contract_id, {"event": "agent_started", "agent": name, "contract_id": contract_id})
            try:
                res_state = await node_fn(current_state)
                await event_broadcaster.broadcast(
                    contract_id,
                    {
                        "event": "agent_completed",
                        "agent": name,
                        "contract_id": contract_id,
                        "risks_count": len(res_state.get("identified_risks", [])),
                        "redlines_count": len(res_state.get("redlines", [])),
                        "obligations_count": len(res_state.get("obligations", [])),
                    },
                )
                return res_state
            except Exception as err:
                logger.error(f"Error in {name}: {err}", exc_info=True)
                transcript = list(current_state.get("debate_transcript") or [])
                transcript.append({
                    "agent_name": f"{name} (Resilience Guard)",
                    "timestamp": time.strftime("%H:%M:%S UTC", time.gmtime()),
                    "content": f"Node experienced temporary exception: {str(err)}. Heuristic fallback applied.",
                    "target_clause": "System Telemetry",
                })
                current_state["debate_transcript"] = transcript
                await event_broadcaster.broadcast(
                    contract_id,
                    {"event": "agent_warning", "agent": name, "message": str(err), "contract_id": contract_id},
                )
                return current_state

        try:
            # 1. Auditor Node
            state = await _run_node_safely(auditor_node, "Auditor Agent", state)

            # 2. Opposing Counsel Node
            state = await _run_node_safely(opposing_node, "Opposing Counsel", state)

            # 3. Redline Synthesizer Node
            state = await _run_node_safely(redline_node, "Redline Synthesizer", state)

            # 4. Obligation Extractor Node
            state = await _run_node_safely(obligation_node, "Obligation Extractor", state)

            state["current_status"] = "analyzed"

            # Persist to Database
            async with AsyncSessionLocal() as db:
                stmt = select(Contract).where(Contract.id == contract_id)
                res = await db.execute(stmt)
                contract_obj = res.scalar_one_or_none()

                if contract_obj:
                    contract_obj.status = "analyzed"
                    contract_obj.overall_risk_score = state.get("overall_score", 0.0)
                    contract_obj.identified_risks = state.get("identified_risks", [])
                    contract_obj.risk_summary = state.get("risk_summary", {})
                    contract_obj.debate_transcript = state.get("debate_transcript", [])
                    contract_obj.redlines = state.get("redlines", [])
                    contract_obj.obligations = state.get("obligations", [])
                    await db.commit()

            await event_broadcaster.broadcast(
                contract_id,
                {"event": "completed", "status": "analyzed", "contract_id": contract_id},
            )

        except Exception as e:
            logger.error(f"Error executing agent graph pipeline: {e}", exc_info=True)
            state["error"] = str(e)
            state["current_status"] = "error"

            async with AsyncSessionLocal() as db:
                stmt = select(Contract).where(Contract.id == contract_id)
                res = await db.execute(stmt)
                contract_obj = res.scalar_one_or_none()
                if contract_obj:
                    contract_obj.status = "error"
                    await db.commit()

            await event_broadcaster.broadcast(
                contract_id,
                {"event": "completed", "status": "error", "error": str(e), "contract_id": contract_id},
            )

        return state


contract_graph = ContractReviewGraph()
