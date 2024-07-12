import pytest
from sqlalchemy import select

from starlette import status

from services.items.models.schema import Item
from v1.routers.item.config import TEST_ITEMS_BASE_URL, DEFAULT_CREATE_ITEM_DATA, DEFAULT_UPDATE_ITEM_DATA
from v1.routers.item.utils import create_default_item


@pytest.mark.asyncio
async def test_fails_case_1(public_client):
    """Unauthorized GET request to the endpoint 'Read all items' returns 401 status code"""
    res = await public_client.get(TEST_ITEMS_BASE_URL)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_fails_case_2(public_client):
    """Unauthorized POST request to the endpoint 'Create item' returns 401 status code"""
    res = await public_client.post(TEST_ITEMS_BASE_URL, json=DEFAULT_CREATE_ITEM_DATA)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_fails_case_3(public_client, db_session):
    """Unauthorized POST request to the endpoint 'Create item' does nit create Item in database"""
    await public_client.post(TEST_ITEMS_BASE_URL, json=DEFAULT_CREATE_ITEM_DATA)

    stmt = select(Item)
    res = await db_session.execute(stmt)
    res = res.scalars().all()
    assert len(res) == 0


@pytest.mark.asyncio
async def test_fails_case_4(public_client):
    """Unauthorized PATCH request to the endpoint 'Partial item update' returns 401 status code"""
    default_data = {
        'name': 'TEst name',
        'description': 'test description',
    }
    item_id = 1
    res = await public_client.patch(url=f'{TEST_ITEMS_BASE_URL}/{item_id}', json=default_data)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_fails_case_5(public_client):
    """Unauthorized GET request to the endpoint 'Read item with special id' returns 401 status code"""
    item_id = 1
    res = await public_client.get(url=f'{TEST_ITEMS_BASE_URL}/{item_id}')
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_fails_case_6(public_client):
    """Unauthorized DELETE request to the endpoint 'Delete item with special id' returns 401 status code"""
    item_id = 1
    res = await public_client.get(url=f'{TEST_ITEMS_BASE_URL}/{item_id}')
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_fails_case_7(public_client, db_session):
    """Unauthorized DELETE request to the endpoint 'Delete item with special id' does not delete the item"""

    item = await create_default_item(db_session, DEFAULT_CREATE_ITEM_DATA)
    item_id = item.id
    await public_client.get(url=f'{TEST_ITEMS_BASE_URL}/{item_id}')

    stmt = select(Item).where(Item.id == item_id)
    item_from_db = await db_session.execute(stmt)
    item_from_db = item_from_db.scalars().first()

    assert item_from_db is not None


@pytest.mark.asyncio
async def test_fails_case_8(public_client, db_session):
    """Unauthorized PATCH request to the endpoint 'Partial update item' with all necessary data
    returns 401 status code and does not update item values"""
    item = await create_default_item(db_session, DEFAULT_CREATE_ITEM_DATA)

    res = await public_client.patch(TEST_ITEMS_BASE_URL + f'/{item.id}', json=DEFAULT_UPDATE_ITEM_DATA)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

    # check new values
    await db_session.refresh(item)
    for k, v in DEFAULT_UPDATE_ITEM_DATA.items():
        assert getattr(item, k) != v
