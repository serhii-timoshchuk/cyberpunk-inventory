from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from configs.app_config import MAIN_PREFIX
from services.security.authorization import get_user_data_from_token
from v1.config import V1_PREFIX

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{MAIN_PREFIX}{V1_PREFIX}/security/token")


def security_dependency(token: Annotated[str, Depends(oauth2_scheme)]):
    """Checks user credentials. Returns UserData, otherwise raises credentials exception"""
    return get_user_data_from_token(token)
