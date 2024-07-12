from typing import Optional

from pydantic import Field, BaseModel, ConfigDict

from services.items.models.enum_models import ItemCategory


class ItemBaseModel(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    name: str
    description: Optional[str] = None
    category: ItemCategory
    quantity: int = Field(ge=0)
    price: float = Field(ge=0)


class ItemReadModel(ItemBaseModel):
    id: int


class ItemCreateModel(ItemBaseModel):
    ...


class ItemPartialUpdateModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[ItemCategory] = None
    quantity: Optional[int] = Field(ge=0, default=None)
    price: Optional[float] = Field(ge=0, default=None)
