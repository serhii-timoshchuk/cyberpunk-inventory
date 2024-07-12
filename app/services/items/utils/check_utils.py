from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from services.items.models.schema import Item
from services.items.utils.get_utils import get_item_by_name, get_item_by_id


async def check_if_item_name_is_unique_or_raise_error(session: AsyncSession, item_name: str) -> None:
    """Returns None if item with special name does not exist, otherwise raises HTTP exception"""
    item = await get_item_by_name(session=session, item_name=item_name)
    if item:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Item with this name already exists")


async def get_item_with_spec_id_or_raise_error(session: AsyncSession, item_id: int) -> Item:
    """Returns Item if item with special id exists, otherwise raises HTTP exception 404"""
    item = await get_item_by_id(session=session, item_id=item_id)

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    return item
