import pytest
from pydantic import ValidationError
from starlette import status

from services.security.token.pydantic_models import TokenResponseModel
from v1.routers.security.config import SECURITY_TOKEN_URL, NONEXISTENT_USER_DATA, EXISTING_USER_DATA


@pytest.mark.asyncio
async def test_fails_case_1(public_client):
    """Unauthorized POST request to the endpoint '/token' with necessary data of nonexistent user
    returns 401 status code"""
    res = await public_client.post(SECURITY_TOKEN_URL, data=NONEXISTENT_USER_DATA)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_successful_case_2(public_client):
    """Unauthorized POST request to the endpoint '/token' with necessary data of existing user
    returns 200 status code"""
    res = await public_client.post(SECURITY_TOKEN_URL, data=EXISTING_USER_DATA)
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_successful_case_3(public_client):
    """Unauthorized POST request to the endpoint '/token' with necessary data of existing user
    returns TokenResponseModel"""
    res = await public_client.post(SECURITY_TOKEN_URL, data=EXISTING_USER_DATA)
    try:
        TokenResponseModel.model_validate(res.json())
    except ValidationError:
        assert False
