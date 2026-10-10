import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.contract import Playbook
from app.schemas.playbook_schemas import PlaybookCreate, PlaybookResponse, PlaybookRule

router = APIRouter(prefix="/playbooks", tags=["Playbooks"])

DEFAULT_PLAYBOOKS = [
    {
        "name": "Standard Corporate Playbook",
        "description": "Balanced enterprise playbook protecting liability, mutual indemnification, and IP retention.",
        "is_default": True,
        "rules": [
            {
                "category": "Indemnification",
                "standard_requirement": "Mutual indemnification capped at 12 months fees.",
                "unacceptable_terms": ["unlimited indemnity", "solely defend and hold harmless"],
                "preferred_fallback": "Cap indemnification to $1,000,000 or fees paid in preceding 12 months.",
                "severity_if_missing": "CRITICAL"
            },
            {
                "category": "Limitation of Liability",
                "standard_requirement": "Consequential damages waiver with aggregate 1x contract value cap.",
                "unacceptable_terms": ["no cap", "uncapped liability"],
                "preferred_fallback": "Cap liability to 1x contract value with carve-outs for confidentiality only.",
                "severity_if_missing": "HIGH"
            }
        ]
    },
    {
        "name": "Aggressive Startup Playbook",
        "description": "High risk tolerance for early deals; focuses strictly on rapid closing and minimal compliance burden.",
        "is_default": False,
        "rules": [
            {
                "category": "Indemnification",
                "standard_requirement": "Accept standard vendor indemnity if overall deal value exceeds $50k.",
                "unacceptable_terms": ["personal liability"],
                "preferred_fallback": "Mutual indemnity capped at $250k.",
                "severity_if_missing": "MEDIUM"
            }
        ]
    }
]


@router.get("/", response_model=List[PlaybookResponse])
async def list_playbooks(db: AsyncSession = Depends(get_db)):
    """List all available playbooks, initializing defaults if none exist."""
    stmt = select(Playbook)
    result = await db.execute(stmt)
    playbooks = result.scalars().all()

    if not playbooks:
        # Initialize default corporate playbooks
        for dp in DEFAULT_PLAYBOOKS:
            pb = Playbook(
                id=str(uuid.uuid4()),
                name=dp["name"],
                description=dp["description"],
                rules=dp["rules"],
                is_default=dp["is_default"]
            )
            db.add(pb)
        await db.commit()
        
        result = await db.execute(select(Playbook))
        playbooks = result.scalars().all()

    response = []
    for pb in playbooks:
        response.append(PlaybookResponse(
            id=pb.id,
            name=pb.name,
            description=pb.description,
            rules=[PlaybookRule(**r) for r in (pb.rules or [])],
            is_default=pb.is_default,
            created_at=pb.created_at
        ))
    return response


@router.post("/", response_model=PlaybookResponse)
async def create_playbook(req: PlaybookCreate, db: AsyncSession = Depends(get_db)):
    """Create a new custom playbook."""
    pb = Playbook(
        id=str(uuid.uuid4()),
        name=req.name,
        description=req.description,
        rules=[r.model_dump() for r in req.rules],
        is_default=req.is_default
    )
    db.add(pb)
    await db.commit()
    await db.refresh(pb)

    return PlaybookResponse(
        id=pb.id,
        name=pb.name,
        description=pb.description,
        rules=[PlaybookRule(**r) for r in pb.rules],
        is_default=pb.is_default,
        created_at=pb.created_at
    )
