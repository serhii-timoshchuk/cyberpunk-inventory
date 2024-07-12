from configs.app_config import ADMIN_USER_NAME
from services.security.exceptions import credentials_exception
from services.security.token.token_utils import decode_access_token
from services.security.user_data.pydantic_models import UserData


def get_user_data_from_token(token: str) -> UserData:
    """Returns user data or raises credentials_exception"""

    payload = decode_access_token(token)
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    if username != ADMIN_USER_NAME:
        raise credentials_exception
    return UserData(username=username)
