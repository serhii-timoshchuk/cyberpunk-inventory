from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.items.models.schema import Item


async def get_item_by_name(session: AsyncSession, item_name: str) -> Union[None, Item]:
    """Returns item if item with special name exists, otherwise returns None"""

    stmt = select(Item).where(Item.name == item_name)
    item = await session.execute(stmt)
    item = item.scalars().first()
    return item


async def get_item_by_id(session: AsyncSession, item_id: int) -> Union[None, Item]:
    """Returns item if item with special name exists, otherwise returns None"""
    stmt = select(Item).where(Item.id == item_id)
    item = await session.execute(stmt)
    item = item.scalars().first()
    return item
