import copy

import pytest
from pydantic import ValidationError
from sqlalchemy import select
from starlette import status

from services.items.models.pydantic_models import ItemReadModel
from services.items.models.schema import Item
from v1.routers.item.config import TEST_ITEMS_BASE_URL, DEFAULT_CREATE_ITEM_DATA
from v1.routers.item.utils import create_default_item


@pytest.mark.asyncio
async def test_successful_case_1(private_client, db_session):
    """POST request with all necessary data by an authorized user returns 201 status code"""
    resp = await private_client.post(TEST_ITEMS_BASE_URL, json=DEFAULT_CREATE_ITEM_DATA)
    assert resp.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_successful_case_2(private_client, db_session):
    """POST request with all necessary data by an authorized user returns ItemReadModel"""
    resp = await private_client.post(TEST_ITEMS_BASE_URL, json=DEFAULT_CREATE_ITEM_DATA)
    resp_item = resp.json()
    assert resp_item is not None
    try:
        ItemReadModel.model_validate(resp_item)
    except ValidationError:
        assert False


@pytest.mark.asyncio
async def test_successful_case_3(private_client, db_session):
    """POST request with all necessary data by an authorized user creates a new Item in the database"""
    await private_client.post(TEST_ITEMS_BASE_URL, json=DEFAULT_CREATE_ITEM_DATA)

    stmt = select(Item).where(Item.name == DEFAULT_CREATE_ITEM_DATA['name'])
    item_from_db = await db_session.execute(stmt)
    item_from_db = item_from_db.scalars().first()

    assert item_from_db is not None

    for k, v in DEFAULT_CREATE_ITEM_DATA.items():
        assert getattr(item_from_db, k) == v


@pytest.mark.asyncio
async def test_fails_case_4(private_client, db_session):
    """A POST request with existing Item name by an authorized user returns 422 and does not create a new Item"""
    # create default item
    await create_default_item(db_session, DEFAULT_CREATE_ITEM_DATA)

    resp = await private_client.post(TEST_ITEMS_BASE_URL, json=DEFAULT_CREATE_ITEM_DATA)

    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    stmt = select(Item)
    items_from_db = await db_session.execute(stmt)
    items_from_db = items_from_db.scalars().all()

    assert len(items_from_db) == 1


@pytest.mark.asyncio
async def test_fails_case_5(private_client, db_session):
    """POST request without Item quantity by an authorized user returns 422 and does not create a new Item"""

    # create default item
    def_data = copy.deepcopy(DEFAULT_CREATE_ITEM_DATA)
    del def_data['quantity']

    resp = await private_client.post(TEST_ITEMS_BASE_URL, json=def_data)

    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    stmt = select(Item)
    items_from_db = await db_session.execute(stmt)
    items_from_db = items_from_db.scalars().all()

    assert len(items_from_db) == 0


@pytest.mark.asyncio
async def test_fails_case_6(private_client, db_session):
    """POST request with Item quantity less than 0 by an authorized user returns 422 and does not create a new Item"""

    # create default item
    def_data = copy.deepcopy(DEFAULT_CREATE_ITEM_DATA)
    def_data['quantity'] = -1

    resp = await private_client.post(TEST_ITEMS_BASE_URL, json=def_data)

    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    stmt = select(Item)
    items_from_db = await db_session.execute(stmt)
    items_from_db = items_from_db.scalars().all()

    assert len(items_from_db) == 0


@pytest.mark.asyncio
async def test_fails_case_7(private_client, db_session):
    """POST request without Item price by an authorized user returns 422 and does not create a new Item"""

    # create default item
    def_data = copy.deepcopy(DEFAULT_CREATE_ITEM_DATA)
    del def_data['price']

    resp = await private_client.post(TEST_ITEMS_BASE_URL, json=def_data)

    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    stmt = select(Item)
    items_from_db = await db_session.execute(stmt)
    items_from_db = items_from_db.scalars().all()

    assert len(items_from_db) == 0


@pytest.mark.asyncio
async def test_fails_case_8(private_client, db_session):
    """POST request with Item price less than 0 by an authorized user returns 422 and does not create a new Item"""

    # create default item
    def_data = copy.deepcopy(DEFAULT_CREATE_ITEM_DATA)
    def_data['price'] = -1

    resp = await private_client.post(TEST_ITEMS_BASE_URL, json=def_data)

    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    stmt = select(Item)
    items_from_db = await db_session.execute(stmt)
    items_from_db = items_from_db.scalars().all()

    assert len(items_from_db) == 0


@pytest.mark.asyncio
async def test_fails_case_9(private_client, db_session):
    """POST request with nonexistent Item category by an authorized user returns 422 and does not create a new Item"""

    # create default item
    def_data = copy.deepcopy(DEFAULT_CREATE_ITEM_DATA)
    def_data['category'] = '111111'

    resp = await private_client.post(TEST_ITEMS_BASE_URL, json=def_data)

    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    stmt = select(Item)
    items_from_db = await db_session.execute(stmt)
    items_from_db = items_from_db.scalars().all()

    assert len(items_from_db) == 0
