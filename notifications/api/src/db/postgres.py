from core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

db_engine = create_async_engine(
    settings.db.url,
    echo=settings.debug,
    future=True,
)

async_session = sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with db_engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_db_session() -> AsyncSession:
    """Create async db session."""
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
