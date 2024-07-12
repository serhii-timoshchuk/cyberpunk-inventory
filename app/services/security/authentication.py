from configs.app_config import ADMIN_USER_NAME, ADMIN_PASSWORD
from services.security.hashing_utils import get_password_hash, verify_password


def authenticate_user(username: str, password: str) -> bool:
    """
    Authenticates a user by comparing their username and hashed password with the stored admin credentials.
    """
    if username != ADMIN_USER_NAME:
        return False

    existing_pass_hash = get_password_hash(ADMIN_PASSWORD)

    if verify_password(password, existing_pass_hash) is False:
        return False
    return True
