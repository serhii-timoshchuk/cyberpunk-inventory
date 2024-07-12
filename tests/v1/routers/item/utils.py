from sqlalchemy.ext.asyncio import AsyncSession

from services.items.models.schema import Item


async def create_default_item(session: AsyncSession, item_data: dict) -> Item:
    """Creates Item wit hDEFAULT_CREATE_ITEM_DATA and returns it"""
    item = Item(**item_data)
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item
