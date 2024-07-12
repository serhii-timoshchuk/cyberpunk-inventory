import pytest
from pydantic import ValidationError
from sqlalchemy import select
from starlette import status

from services.items.models.pydantic_models import ItemReadModel
from services.items.models.schema import Item
from v1.routers.item.config import TEST_ITEMS_BASE_URL, DEFAULT_CREATE_ITEM_DATA


@pytest.mark.asyncio
async def test_successful_case_1(private_client):
    """A successful request by an authorized user returns status code 200 """
    res = await private_client.get(TEST_ITEMS_BASE_URL)
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_successful_case_2(private_client, db_session):
    """A successful query by an authorized user returns an empty list if there are no Items in the database"""

    # check db is empty
    stmt = select(Item)
    items = await db_session.execute(stmt)
    items = items.scalars().all()
    assert len(items) == 0

    res = await private_client.get(TEST_ITEMS_BASE_URL)
    res_list = res.json()
    assert isinstance(res_list, list)
    assert len(res_list) == 0


@pytest.mark.asyncio
async def test_successful_case_3(private_client, db_session):
    """A successful request by an authorized user returns List of ItemReadModel if some models exists"""
    # create Item
    item = Item(**DEFAULT_CREATE_ITEM_DATA)
    db_session.add(item)
    await db_session.commit()

    res = await private_client.get(TEST_ITEMS_BASE_URL)
    res_list = res.json()
    assert isinstance(res_list, list)
    try:
        ItemReadModel.model_validate(res.json()[0])
    except ValidationError:
        assert False
    assert len(res_list) == 1


@pytest.mark.asyncio
async def test_successful_case_4(private_client, db_session):
    """A successful request with pagination parameters by an authorized user
    returns List of ItemReadModel if some models exists"""
    # create Item
    item_1 = Item(**DEFAULT_CREATE_ITEM_DATA)
    item_2 = Item(**DEFAULT_CREATE_ITEM_DATA)
    item_2.name = 'Another unique name'
    db_session.add(item_1)
    db_session.add(item_2)
    await db_session.commit()
    await db_session.refresh(item_2)

    # mus return list with only last item
    res = await private_client.get(TEST_ITEMS_BASE_URL, params={'limit': 1, 'offset': 1})
    res_list = res.json()
    assert len(res_list) == 1

    res_item = res_list[0]
    # Check item data
    for k, v in res_item.items():
        assert getattr(item_2, k) == v
