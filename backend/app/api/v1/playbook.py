from typing import List, Dict, Optional
from fastapi import APIRouter, HTTPException
from app.schemas.playbook_schemas import Playbook, PlaybookRule

router = APIRouter()

STANDARD_PLAYBOOKS = [
    Playbook(
        id="strict_enterprise",
        name="Strict Enterprise Playbook",
        description="Zero tolerance for uncapped indemnification, offshore venue, or foundational AI training on telemetry.",
        rules=[
            PlaybookRule(
                category="AI Training",
                severity="CRITICAL",
                preferred_position="Strict prohibition on customer data retention for model weights.",
                fallback_position="Zero retention beyond runtime token generation.",
                hard_stop="No ingestion of raw prompts or customer datasets.",
            ),
            PlaybookRule(
                category="Indemnification",
                severity="CRITICAL",
                preferred_position="True deductible basket capped at 1.0x annual fees.",
                fallback_position="Mutual indemnification capped at 1.5x annual fees.",
                hard_stop="No first-dollar tipping baskets.",
            ),
            PlaybookRule(
                category="Limitation of Liability",
                severity="HIGH",
                preferred_position="12-month trailing fees cap with 2x super-cap for data breaches.",
                fallback_position="Aggregate liability capped at contract value.",
                hard_stop="No uncapped indirect damages.",
            ),
        ],
    ),
    Playbook(
        id="standard_corporate",
        name="Standard Corporate Playbook",
        description="Balanced enterprise posture for Fortune 500 SaaS and commercial procurement.",
        rules=[
            PlaybookRule(
                category="AI Training",
                severity="HIGH",
                preferred_position="De-identified telemetry only with opt-out right.",
                fallback_position="Aggregated system performance logs only.",
                hard_stop="No customer PII retention.",
            ),
            PlaybookRule(
                category="Indemnification",
                severity="HIGH",
                preferred_position="Mutual third-party IP defense.",
                fallback_position="IP defense capped at 2x annual contract value.",
                hard_stop="No unilateral uncapped defense.",
            ),
        ],
    ),
    Playbook(
        id="founder_friendly",
        name="Founder Friendly Playbook",
        description="Speed-to-close posture designed to minimize friction while preserving core IP and cash flow.",
        rules=[
            PlaybookRule(
                category="IP Ownership",
                severity="CRITICAL",
                preferred_position="Developer retains background IP, licenses deliverables.",
                fallback_position="Joint ownership with free cross-licensing.",
                hard_stop="No assignment of pre-existing core tech.",
            ),
            PlaybookRule(
                category="Payment",
                severity="HIGH",
                preferred_position="Net 15 with 1.5% late payment interest.",
                fallback_position="Net 30 undisputed.",
                hard_stop="No payment delays exceeding 45 days.",
            ),
        ],
    ),
]

# User custom playbooks registry
CUSTOM_PLAYBOOKS: Dict[str, Playbook] = {}


@router.get("/", response_model=List[Playbook])
async def list_playbooks():
    """List institutional negotiation playbooks including custom playbooks."""
    return STANDARD_PLAYBOOKS + list(CUSTOM_PLAYBOOKS.values())


@router.get("/custom", response_model=List[Playbook])
async def list_custom_playbooks():
    """List only user-defined custom playbooks."""
    return list(CUSTOM_PLAYBOOKS.values())


@router.post("/custom", response_model=Playbook)
async def create_custom_playbook(playbook: Playbook):
    """Create or update a custom negotiation playbook."""
    pb_id = playbook.id.lower().replace(" ", "_")
    playbook.id = pb_id
    CUSTOM_PLAYBOOKS[pb_id] = playbook
    return playbook


@router.delete("/custom/{id}")
async def delete_custom_playbook(id: str):
    """Delete a custom negotiation playbook."""
    pb_id = id.lower().replace(" ", "_")
    if pb_id in CUSTOM_PLAYBOOKS:
        del CUSTOM_PLAYBOOKS[pb_id]
        return {"status": "success", "message": f"Playbook '{id}' deleted"}
    raise HTTPException(status_code=404, detail=f"Custom playbook '{id}' not found")


@router.get("/{id}", response_model=Playbook)
async def get_playbook(id: str):
    """Retrieve details for specific playbook."""
    pb_id = id.lower().replace(" ", "_")
    if pb_id in CUSTOM_PLAYBOOKS:
        return CUSTOM_PLAYBOOKS[pb_id]
    for pb in STANDARD_PLAYBOOKS:
        if pb.id == id or pb.name.lower() == id.lower() or pb.id == pb_id:
            return pb
    return STANDARD_PLAYBOOKS[0]
