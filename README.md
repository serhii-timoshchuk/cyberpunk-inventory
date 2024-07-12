# cyberpunk-inventory
Cyberpunk Inventory Management System


# Environment variables
## General

APP_TITLE = application title (Cyberpunk Inventory - by default)

MAIN_PREFIX = main prefix for endpoints (/api - by default)

## Database configs

DB_USER = database username (postgres - by default)

DB_PASS = database user password (postgres - by default)

DB_HOST = database host (localhost - by default)

DB_PORT = database port (5432 - by default)

DB_NAME = database name (inventory - by default)


## Security configs
ADMIN_USER_NAME = username with admin access rights (Admin - by default)

ADMIN_PASSWORD = password for admin user (Admin password - by default)

# Token configs
TOKEN_SECRET_KEY = secret key for tokens - openssl rand -hex 32 (09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7 - by default)

TOKEN_ALGORITHM = encrypt algorithm for tokens (HS256 - by default)

ACCESS_TOKEN_EXPIRE_MINUTES = token lifetime in minutes (30 - by default)


# How to run app

## Without docker

1) Set the values of the database variables in accordance with your database
2) From the base folder install all requirements:

    ``pip install -r requirements.txt``
3) From the 'app' folder run migrations:

    ``alembic upgrade head``
4) From the 'app' run app:
    ``uvicorn main:app``
5) go to http://127.0.0.1:8000/ in your browser
## With docker-compose

1) From the base folder run build and run docker-compose:

    ``docker-compose build``
    ``docker-compose up``
2) Go to http://127.0.0.1:8000/ in your browser

# How to run tests
To run tests, you need a Docker-API compatible container runtime, such as using Testcontainers Cloud or installing Docker locally

1) From the 'tests' folder install all test_requirements:
    
    ``pip install -r test_requirements.txt``
2) Run tests:

    ``pytest``
