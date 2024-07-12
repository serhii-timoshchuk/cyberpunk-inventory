from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import session_maker


async def get_session() -> AsyncSession:
    """Yields AsyncSession object"""
    async with session_maker() as session:
        yield session
