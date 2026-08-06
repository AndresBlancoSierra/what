from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from what.config.settings import settings
from what.database.models import Base

_engine = None
_session_factory = None


async def get_engine():
    global _engine
    if _engine is None:
        _engine = create_async_engine(settings.db_url, echo=False)
    return _engine


async def get_session() -> AsyncSession:
    global _session_factory, _engine
    if _session_factory is None:
        eng = await get_engine()
        _session_factory = async_sessionmaker(eng, expire_on_commit=False)
    return _session_factory()


async def init_db():
    eng = await get_engine()
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def dispose_db():
    global _engine, _session_factory
    if _engine:
        await _engine.dispose()
        _engine = None
        _session_factory = None
