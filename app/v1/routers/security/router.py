from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from configs.app_config import ACCESS_TOKEN_EXPIRE_MINUTES
from services.security.authentication import authenticate_user
from services.security.forms import token_form
from services.security.token.pydantic_models import TokenResponseModel
from services.security.token.token_utils import create_access_token

security_prefix = '/security'
router = APIRouter(prefix=security_prefix)
routers_tag = 'Security'


@router.post("/token", status_code=status.HTTP_200_OK, tags=[routers_tag], response_model=TokenResponseModel)
async def get_access_token(form_data: Annotated[token_form, Depends()]):
    is_authenticated = authenticate_user(username=form_data.username, password=form_data.password)
    if is_authenticated is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return TokenResponseModel(access_token=access_token, token_type="bearer")
