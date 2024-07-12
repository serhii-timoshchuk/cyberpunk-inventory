import copy
import pytest
from sqlalchemy.exc import IntegrityError

from services.items.models.enum_models import ItemCategory
from services.items.models.schema import Item

DEFAULT_DATA = {
    'name': 'TEst name',
    'description': 'test description',
    'category': ItemCategory.WEAPON.value,
    'quantity': 1,
    'price': 10.5
}


@pytest.mark.asyncio
async def test_fails_case_1(db_session):
    """Can`t create Item without name"""
    default_data = copy.deepcopy(DEFAULT_DATA)
    del default_data['name']
    item = Item(**default_data)
    db_session.add(item)
    with pytest.raises(IntegrityError):
        await db_session.commit()


@pytest.mark.asyncio
async def test_fails_case_2(db_session):
    """Can`t create Item without category"""
    default_data = copy.deepcopy(DEFAULT_DATA)
    del default_data['category']
    item = Item(**default_data)
    db_session.add(item)
    with pytest.raises(IntegrityError):
        await db_session.commit()


@pytest.mark.asyncio
async def test_fails_case_3(db_session):
    """Can`t create Item without quantity"""
    default_data = copy.deepcopy(DEFAULT_DATA)
    del default_data['quantity']
    item = Item(**default_data)
    db_session.add(item)
    with pytest.raises(IntegrityError):
        await db_session.commit()


@pytest.mark.asyncio
async def test_fails_case_4(db_session):
    """Can`t create Item without price"""
    default_data = copy.deepcopy(DEFAULT_DATA)
    del default_data['price']
    item = Item(**default_data)
    db_session.add(item)
    with pytest.raises(IntegrityError):
        await db_session.commit()


@pytest.mark.asyncio
async def test_fails_case_5(db_session):
    """Can`t create Item with price less than 0"""
    default_data = copy.deepcopy(DEFAULT_DATA)
    default_data['quantity'] = -2
    with pytest.raises(ValueError):
        Item(**default_data)


@pytest.mark.asyncio
async def test_fails_case_6(db_session):
    """Can`t create Item with quantity less than 0"""
    default_data = copy.deepcopy(DEFAULT_DATA)
    default_data['quantity'] = -2
    with pytest.raises(ValueError):
        Item(**default_data)


@pytest.mark.asyncio
async def test_successful_case_7(db_session):
    """Creates Item with all necessary attributes"""
    item = Item(**DEFAULT_DATA)
    db_session.add(item)
    await db_session.commit()
    assert True
