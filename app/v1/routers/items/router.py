from typing import List

from fastapi import APIRouter, Depends, Query, Path, Body, HTTPException
from sqlalchemy import select, asc
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from db.session import get_session

from services.items.models.pydantic_models import ItemReadModel, ItemCreateModel, ItemPartialUpdateModel
from services.items.models.schema import Item
from services.items.utils.check_utils import check_if_item_name_is_unique_or_raise_error, \
    get_item_with_spec_id_or_raise_error

from v1.security import security_dependency

items_prefix = '/items'
router = APIRouter(prefix=items_prefix, dependencies=[Depends(security_dependency)])
routers_tag = 'Items'


@router.get('', tags=[routers_tag], status_code=status.HTTP_200_OK, response_model=List[ItemReadModel])
async def get_items(session: AsyncSession = Depends(get_session),
                    offset: int = Query(ge=0, default=0),
                    limit: int = Query(ge=1, default=20)):
    """Read all items"""
    stmt = select(Item).order_by(asc(Item.id)).offset(offset).limit(limit)
    items = await session.execute(stmt)
    items = items.scalars().all()
    return items


@router.post('', tags=[routers_tag], status_code=status.HTTP_201_CREATED, response_model=ItemReadModel)
async def create_item(item: ItemCreateModel, session: AsyncSession = Depends(get_session)):
    """Create a new item"""
    # check if item with name exists
    await check_if_item_name_is_unique_or_raise_error(session=session, item_name=item.name)

    new_item = Item(**item.model_dump(exclude_unset=True, exclude_defaults=True))
    session.add(new_item)
    await session.commit()
    await session.refresh(new_item)
    return new_item


@router.get('/{item_id}', tags=[routers_tag], status_code=status.HTTP_200_OK, response_model=ItemReadModel)
async def get_item_by_id(session: AsyncSession = Depends(get_session),
                         item_id: int = Path()):
    """Read item with special id"""

    item = await get_item_with_spec_id_or_raise_error(session=session, item_id=item_id)
    return item


@router.patch('/{item_id}', tags=[routers_tag], status_code=status.HTTP_200_OK, response_model=ItemReadModel)
async def partial_item_update(item_id: int = Path(), item: ItemPartialUpdateModel = Body(...),
                              session: AsyncSession = Depends(get_session)):
    """Item partial update"""
    item_from_db = await get_item_with_spec_id_or_raise_error(session=session, item_id=item_id)

    # check if name already exists
    if item.name:
        stmt = select(Item).where(Item.name == item.name, Item.id != item_from_db.id)
        item_with_name = await session.execute(stmt)
        item_with_name = item_with_name.first()

        if item_with_name:
            raise HTTPException(status_code=422, detail="Item with this name already exists")

    for key, value in item.model_dump(exclude_unset=True, exclude_defaults=True).items():
        setattr(item_from_db, key, value)

    session.add(item_from_db)
    await session.commit()

    return item_from_db


@router.delete('/{item_id}', tags=[routers_tag], status_code=status.HTTP_204_NO_CONTENT)
async def delete_item_by_id(session: AsyncSession = Depends(get_session),
                            item_id: int = Path()):
    """Delete item with special id"""

    item = await get_item_with_spec_id_or_raise_error(session=session, item_id=item_id)

    await session.delete(item)
    await session.commit()
    return
