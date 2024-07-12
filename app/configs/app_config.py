import os

# FASTAPI configs
APP_TITLE = os.environ.get("APP_TITLE", "Cyberpunk Inventory")
MAIN_PREFIX = '/api'


# Database configs
DB_TYPE = 'postgresql+asyncpg'
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASS = os.environ.get("DB_PASS", "postgres")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "inventory")
ASYNC_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# Security configs
ADMIN_USER_NAME = os.environ.get("ADMIN_USER_NAME", 'Admin')
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", 'Admin password')

# Token configs
# openssl rand -hex 32
TOKEN_SECRET_KEY = os.environ.get("TOKEN_SECRET_KEY",
                                  '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7')
TOKEN_ALGORITHM = os.environ.get("TOKEN_ALGORITHM", 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
