import os
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import init_db
from app.api.v1.contracts import router as contracts_router
from app.api.v1.analysis import router as analysis_router
from app.api.v1.playbook import router as playbook_router
from app.api.v1.stream import router as stream_router
from app.api.v1.auth import router as auth_router
from app.mcp_server.server import mcp_server


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB schema on startup
    await init_db()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Autonomous Multi-Agent Legal AI Studio",
    lifespan=lifespan,
)

# CORS configuration for Frontend, Studio and Vercel Tunnels
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1|.*\.vercel\.app)(:[0-9]+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# API Routers
app.include_router(contracts_router, prefix="/api/v1/contracts", tags=["Contracts"])
app.include_router(analysis_router, prefix="/api/v1/analysis", tags=["Analysis"])
app.include_router(playbook_router, prefix="/api/v1/playbook", tags=["Playbooks"])
app.include_router(stream_router, prefix="/api/v1/stream", tags=["Streaming"])
app.include_router(auth_router, prefix="/api/v1", tags=["Authentication"])


# MCP Endpoints (JSON-RPC Tools Gateway)
@app.get("/mcp/tools", tags=["MCP"])
async def mcp_list_tools():
    """List tools exposed via Model Context Protocol (MCP)."""
    return {"tools": mcp_server.list_tools()}


@app.post("/mcp/call", tags=["MCP"])
async def mcp_call_tool(payload: Dict[str, Any]):
    """Execute tool call via Model Context Protocol (MCP)."""
    name = payload.get("name") or payload.get("tool_name")
    arguments = payload.get("arguments") or payload.get("args") or {}
    if not name:
        return {"error": "Missing 'name' in MCP payload"}
    try:
        res = mcp_server.call_tool(name, arguments)
        return {"result": res}
    except Exception as e:
        return {"error": str(e)}


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": settings.VERSION}


# Serve UI
STATIC_DIR = settings.BASE_DIR / "static"
INDEX_FILE = STATIC_DIR / "index.html"


@app.get("/", response_class=HTMLResponse, tags=["Studio"])
@app.get("/studio", response_class=HTMLResponse, tags=["Studio"])
async def serve_studio():
    """Serves the ContractMind v1.5 Alpine.js Neo-Legal Studio."""
    if INDEX_FILE.exists():
        return FileResponse(INDEX_FILE, media_type="text/html")
    return HTMLResponse("<h1>ContractMind v1.5 Studio</h1><p>Building UI...</p>")


if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
