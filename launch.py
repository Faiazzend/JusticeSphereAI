import os
import sys
import asyncio
import logging
import threading
import webbrowser
from pathlib import Path

# Add backend directory to sys.path
BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.config import settings
from app.database import init_db


def setup_environment():
    """Ensure all required runtime directories exist."""
    print("==================================================")
    print(" ContractMind v1.5 — Autonomous Multi-Agent AI Studio")
    print(" Track: JusticeSphere_AI | AI Builders Congress 2026")
    print("==================================================")

    settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
    settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    settings.EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    settings.CHROMA_PERSIST_DIR.mkdir(parents=True, exist_ok=True)

    log_file = BACKEND_DIR / "backend.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(str(log_file), encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )
    logging.info("Initialized storage directories and backend logging.")


async def migrate_database():
    """Run database schema migration and initialization."""
    print("Running database schema migration...")
    await init_db()
    print("Database schema initialized successfully.")


def open_browser():
    """Open default web browser to the ContractMind studio."""
    url = "http://localhost:8000"
    print(f"Opening browser at {url}...")
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Could not open browser automatically: {e}")


def main():
    setup_environment()
    asyncio.run(migrate_database())

    # Schedule browser opening
    timer = threading.Timer(1.5, open_browser)
    timer.daemon = True
    timer.start()

    # Launch Uvicorn
    import uvicorn
    print("Starting Uvicorn server on http://0.0.0.0:8000 ...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        app_dir=str(BACKEND_DIR),
        reload=False,
    )


if __name__ == "__main__":
    main()
