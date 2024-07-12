from configs.app_config import MAIN_PREFIX
from services.items.models.enum_models import ItemCategory
from v1.config import V1_PREFIX
from v1.routers.items.router import items_prefix

TEST_ITEMS_BASE_URL = f'{MAIN_PREFIX}{V1_PREFIX}{items_prefix}'

DEFAULT_CREATE_ITEM_DATA = {
    'name': 'Test name',
    'description': 'test description',
    'category': ItemCategory.WEAPON.value,
    'quantity': 1,
    'price': 10.5
}

DEFAULT_UPDATE_ITEM_DATA = {
    'name': 'Updated name',
    'description': 'updated test description',
    'category': ItemCategory.GADGET.value,
    'quantity': 5,
    'price': 155.4
}
