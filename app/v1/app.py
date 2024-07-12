from fastapi import FastAPI

from configs.app_config import APP_TITLE
from v1.routers.items.router import router as item_router
from v1.routers.security.router import router as security_router


v1_app = FastAPI(title=APP_TITLE)
v1_app.include_router(item_router)
v1_app.include_router(security_router)
