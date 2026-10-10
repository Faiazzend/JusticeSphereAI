from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.contracts import router as contracts_router
from app.api.v1.analysis import router as analysis_router
from app.api.v1.stream import router as stream_router
from app.api.v1.playbook import router as playbook_router

api_v1_router = APIRouter()
api_v1_router.include_router(auth_router)
api_v1_router.include_router(contracts_router)
api_v1_router.include_router(analysis_router)
api_v1_router.include_router(stream_router)
api_v1_router.include_router(playbook_router)
