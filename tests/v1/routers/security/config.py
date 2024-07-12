from configs.app_config import MAIN_PREFIX, ADMIN_USER_NAME, ADMIN_PASSWORD
from v1.config import V1_PREFIX
from v1.routers.security.router import security_prefix

TEST_SECURITY_BASE_URL = f'{MAIN_PREFIX}{V1_PREFIX}{security_prefix}'
SECURITY_TOKEN_URL = f'{TEST_SECURITY_BASE_URL}/token'


EXISTING_USER_DATA = {'username': ADMIN_USER_NAME, 'password': ADMIN_PASSWORD}
NONEXISTENT_USER_DATA = {'username': 'test user', 'password': 'test password'}
