from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=False,
    connect_args={"check_same_thread": False},
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db() -> None:
    # Ensure directory exists
    settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
    async with engine.begin() as conn:
        # Import models to ensure they are registered with Base.metadata
        from app.models.contract import Contract  # noqa: F401
        from app.models.audit import AuditLog  # noqa: F401
        from app.models.user import User  # noqa: F401

        await conn.run_sync(Base.metadata.create_all)
        # Auto-migrate columns if database was pre-initialized in older versions
        try:
            await conn.exec_driver_sql("ALTER TABLE users ADD COLUMN hashed_password VARCHAR(255) DEFAULT ''")
        except Exception:
            pass
