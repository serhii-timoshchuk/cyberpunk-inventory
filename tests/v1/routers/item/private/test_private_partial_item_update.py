import copy

import pytest
from pydantic import ValidationError
from starlette import status

from services.items.models.pydantic_models import ItemReadModel
from v1.routers.item.config import TEST_ITEMS_BASE_URL, DEFAULT_CREATE_ITEM_DATA, DEFAULT_UPDATE_ITEM_DATA
from v1.routers.item.utils import create_default_item


@pytest.mark.asyncio
async def test_successful_case_1(private_client, db_session):
    """PATCH request with all necessary data by an authorized user returns 200 status code"""
    item = await create_default_item(db_session, DEFAULT_CREATE_ITEM_DATA)
    resp = await private_client.patch(TEST_ITEMS_BASE_URL + f'/{item.id}', json=DEFAULT_UPDATE_ITEM_DATA)
    assert resp.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_successful_case_2(private_client, db_session):
    """PATCH request with all necessary data by an authorized user returns ItemReadModel with updated values"""
    item = await create_default_item(db_session, DEFAULT_CREATE_ITEM_DATA)

    resp = await private_client.patch(TEST_ITEMS_BASE_URL + f'/{item.id}', json=DEFAULT_UPDATE_ITEM_DATA)
    resp_item = resp.json()
    assert resp_item is not None

    try:
        ItemReadModel.model_validate(resp_item)
    except ValidationError:
        assert False

    # check new values
    await db_session.refresh(item)
    for k, v in DEFAULT_UPDATE_ITEM_DATA.items():
        assert getattr(item, k) == v


@pytest.mark.asyncio
async def test_fails_case_3(private_client, db_session):
    """A PATCH request with existing Item name by an authorized user returns 422 and does not update the Item"""
    # create default item
    def_data = copy.deepcopy(DEFAULT_CREATE_ITEM_DATA)
    item = await create_default_item(db_session, def_data)
    existing_name = 'another item name'
    def_data['name'] = existing_name
    await create_default_item(db_session, def_data)

    def_upd_data = copy.deepcopy(DEFAULT_UPDATE_ITEM_DATA)
    def_upd_data['name'] = existing_name
    resp = await private_client.patch(TEST_ITEMS_BASE_URL + f'/{item.id}', json=def_upd_data)

    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    db_session.refresh(item)
    for k, v in DEFAULT_UPDATE_ITEM_DATA.items():
        assert getattr(item, k) != v


@pytest.mark.asyncio
async def test_successful_case_4(private_client, db_session):
    """PATCH request only with Item name by an authorized user returns 200 and updates Item.name"""
    item = await create_default_item(db_session, DEFAULT_CREATE_ITEM_DATA)
    new_value = DEFAULT_UPDATE_ITEM_DATA['name']
    assert item.name != new_value
    payload = {'name': new_value}

    resp = await private_client.patch(TEST_ITEMS_BASE_URL + f'/{item.id}', json=payload)

    assert resp.status_code == status.HTTP_200_OK

    await db_session.refresh(item)

    assert item.name == new_value


@pytest.mark.asyncio
async def test_successful_case_5(private_client, db_session):
    """PATCH request only with Item description by an authorized user returns 200 and updates Item.description"""
    item = await create_default_item(db_session, DEFAULT_CREATE_ITEM_DATA)
    new_value = DEFAULT_UPDATE_ITEM_DATA['description']
    assert item.description != new_value
    payload = {'description': new_value}

    resp = await private_client.patch(TEST_ITEMS_BASE_URL + f'/{item.id}', json=payload)

    assert resp.status_code == status.HTTP_200_OK

    await db_session.refresh(item)

    assert item.description == new_value


@pytest.mark.asyncio
async def test_successful_case_6(private_client, db_session):
    """PATCH request only with Item category by an authorized user returns 200 and updates Item.category"""
    item = await create_default_item(db_session, DEFAULT_CREATE_ITEM_DATA)
    new_value = DEFAULT_UPDATE_ITEM_DATA['category']
    assert item.category != new_value
    payload = {'category': new_value}

    resp = await private_client.patch(TEST_ITEMS_BASE_URL + f'/{item.id}', json=payload)

    assert resp.status_code == status.HTTP_200_OK

    await db_session.refresh(item)

    assert item.category == new_value


@pytest.mark.asyncio
async def test_successful_case_7(private_client, db_session):
    """PATCH request only with Item price by an authorized user returns 200 and updates Item.price"""
    item = await create_default_item(db_session, DEFAULT_CREATE_ITEM_DATA)
    new_value = DEFAULT_UPDATE_ITEM_DATA['price']
    assert item.price != new_value
    payload = {'price': new_value}

    resp = await private_client.patch(TEST_ITEMS_BASE_URL + f'/{item.id}', json=payload)

    assert resp.status_code == status.HTTP_200_OK

    await db_session.refresh(item)

    assert item.price == new_value


@pytest.mark.asyncio
async def test_successful_case_8(private_client, db_session):
    """PATCH request only with Item quantity by an authorized user returns 200 and updates Item.quantity"""
    item = await create_default_item(db_session, DEFAULT_CREATE_ITEM_DATA)
    new_value = DEFAULT_UPDATE_ITEM_DATA['quantity']
    assert item.quantity != new_value
    payload = {'quantity': new_value}

    resp = await private_client.patch(TEST_ITEMS_BASE_URL + f'/{item.id}', json=payload)

    assert resp.status_code == status.HTTP_200_OK

    await db_session.refresh(item)

    assert item.quantity == new_value


@pytest.mark.asyncio
async def test_fails_case_9(private_client, db_session):
    """PATCH request with unavailable Item category by an authorized user returns 422
    and does not update Item.category"""
    item = await create_default_item(db_session, DEFAULT_CREATE_ITEM_DATA)
    new_value = '11111'

    payload = {'category': new_value}

    resp = await private_client.patch(TEST_ITEMS_BASE_URL + f'/{item.id}', json=payload)

    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    await db_session.refresh(item)

    assert item.category != new_value


@pytest.mark.asyncio
async def test_fails_case_10(private_client, db_session):
    """PATCH request with Item price less than 0 by an authorized user returns 422 and does not update Item.price"""
    item = await create_default_item(db_session, DEFAULT_CREATE_ITEM_DATA)
    new_value = -1

    payload = {'price': new_value}

    resp = await private_client.patch(TEST_ITEMS_BASE_URL + f'/{item.id}', json=payload)

    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    await db_session.refresh(item)

    assert item.price != new_value


@pytest.mark.asyncio
async def test_fails_case_11(private_client, db_session):
    """PATCH request with Item quantity less than 0 by an authorized user returns 422 and
    does not update Item.quantity"""
    item = await create_default_item(db_session, DEFAULT_CREATE_ITEM_DATA)
    new_value = -1

    payload = {'quantity': new_value}

    resp = await private_client.patch(TEST_ITEMS_BASE_URL + f'/{item.id}', json=payload)

    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    await db_session.refresh(item)

    assert item.quantity != new_value
