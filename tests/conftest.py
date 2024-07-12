import sys
import os

from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from pytest_asyncio import fixture

from testcontainers.postgres import PostgresContainer

sys.path.append(os.path.join(sys.path[0], '..', 'app'))

# import all db models - to get full Base
from services.items.models.schema import Base # noqa


class DBContainer(PostgresContainer):
    def get_connection_url(self, host=None):
        if not host:
            host = 'localhost'
        return super().get_connection_url(host=host)


def get_db_image_config():
    config = {'image': 'postgres:latest',
              'port': 5432,
              'user': 'test_admin',
              'password': 'test_pass',
              'dbname': 'inventory'
              }
    return config


@fixture(scope='session', autouse=True)
def postgres_instance():
    config = get_db_image_config()
    postgres_container = DBContainer(**config)
    with postgres_container as container:
        yield container
        container.volumes.clear()


@fixture(scope='function')
async def engine(postgres_instance):
    db_url = postgres_instance.get_connection_url()
    db_url = db_url.replace('psycopg2', 'asyncpg')
    db_engine = create_async_engine(db_url, poolclass=StaticPool, echo=False)
    yield db_engine

    await db_engine.dispose()


@fixture(scope='function')
async def db_session(engine):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

        session_maker = async_sessionmaker(engine, expire_on_commit=False, autoflush=False, autocommit=False)
        async with session_maker() as session:
            yield session

        await connection.run_sync(Base.metadata.drop_all)
