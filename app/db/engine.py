from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from configs.app_config import ASYNC_DATABASE_URL

async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=False, pool_size=20, max_overflow=100)
session_maker = async_sessionmaker(async_engine, expire_on_commit=False, autoflush=False, autocommit=False)
