from httpx import AsyncClient, ASGITransport
from pytest_asyncio import fixture
from configs.app_config import MAIN_PREFIX, ADMIN_USER_NAME, ADMIN_PASSWORD
from v1.config import V1_PREFIX
from v1.routers.security.router import security_prefix


@fixture(scope='function')
async def public_client(db_session, engine):
    from db.session import get_session
    from main import v1_app, app

    app.dependency_overrides[get_session] = lambda: db_session
    v1_app.dependency_overrides[get_session] = lambda: db_session

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
    v1_app.dependency_overrides.clear()


@fixture(scope='function')
async def private_client(db_session, engine):
    from db.session import get_session
    from main import v1_app, app

    app.dependency_overrides[get_session] = lambda: db_session
    v1_app.dependency_overrides[get_session] = lambda: db_session

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # get token
        token_data = await client.post(f'{MAIN_PREFIX}{V1_PREFIX}{security_prefix}/token',
                                       data={'username': ADMIN_USER_NAME, 'password': ADMIN_PASSWORD})
        token = token_data.json()['access_token']
        headers = {"Authorization": f"Bearer {token}"}

        client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test", headers=headers)
        yield client

    app.dependency_overrides.clear()
    v1_app.dependency_overrides.clear()
