import pytest
from sqlalchemy import select
from starlette import status

from services.items.models.schema import Item
from v1.routers.item.config import TEST_ITEMS_BASE_URL, DEFAULT_CREATE_ITEM_DATA
from v1.routers.item.utils import create_default_item


@pytest.mark.asyncio
async def test_failed_case_1(private_client, db_session):
    """A request with nonexistent Item id by an authorized user returns 404 status code"""
    # check Item with id doesn't exist
    item_id = 99999

    stmt = select(Item).where(Item.id == item_id)
    res = await db_session.execute(stmt)
    res = res.scalars().first()
    assert res is None

    res = await private_client.get(TEST_ITEMS_BASE_URL + f'/{item_id}')
    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_successful_case_2(private_client, db_session):
    """A request with existing Item id by an authorized user returns 200 status code"""
    # create item
    item = await create_default_item(db_session, DEFAULT_CREATE_ITEM_DATA)

    res = await private_client.get(TEST_ITEMS_BASE_URL + f'/{item.id}')
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_successful_case_3(private_client, db_session):
    """A request with existing Item id by an authorized user returns ItemReadModel"""
    # create item
    item = await create_default_item(db_session, DEFAULT_CREATE_ITEM_DATA)

    res = await private_client.get(TEST_ITEMS_BASE_URL + f'/{item.id}')
    resp_item_data = res.json()
    assert resp_item_data is not None

    for k, v in resp_item_data.items():
        assert getattr(item, k) == v
