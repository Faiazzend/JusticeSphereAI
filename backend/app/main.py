from contextlib import asynccontextmanager
from typing import Dict, Any
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
from app.database import init_db
from app.api import api_v1_router
from app.mcp_server import mcp_server


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite database and default schema
    await init_db()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-Native Contract Intelligence, Multi-Agent Redlining & Obligation Extraction Engine",
    lifespan=lifespan
)

# CORS configuration for Frontend and Tunnels
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

# Include v1 API routes
app.include_router(api_v1_router, prefix=settings.API_V1_STR)


import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
@app.get("/index.html")
@app.get("/studio")
async def root():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(
            index_file,
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate, max-age=0",
                "Pragma": "no-cache",
                "Expires": "0",
            }
        )
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "operational",
        "docs_url": "/docs",
        "mcp_endpoint": "/mcp/tools"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.VERSION}


# -------------------------------------------------------------
# MCP Server HTTP / JSON-RPC Gateway Endpoints
# -------------------------------------------------------------
@app.get("/mcp/tools")
async def get_mcp_tools():
    """Returns list of exposed tools conforming to Model Context Protocol."""
    return {"tools": mcp_server.list_tools()}


@app.post("/mcp/call")
async def call_mcp_tool(req: Request):
    """Executes an MCP tool call."""
    body = await req.json()
    tool_name = body.get("name")
    arguments = body.get("arguments", {})
    result = mcp_server.call_tool(tool_name, arguments)
    return {"result": result}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
