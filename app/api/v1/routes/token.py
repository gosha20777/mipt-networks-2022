import logging
from typing import Union

from fastapi import APIRouter
from fastapi.params import Depends

from api.v1.models.tokem import (
    AccessTokenResponse,
    SignInRequest,
    TokenIssuerResponse,
    TokenResponse,
)
from core.db.definition import get_db
from core.services import tocken_service as service

router = APIRouter()
logger = logging.getLogger('token_api')
db = get_db()


@router.post(
    '/token', 
    response_model=Union[TokenResponse, TokenIssuerResponse]
)
def create_token(
        content: SignInRequest,
        sess=Depends(db.get_session)
) -> TokenIssuerResponse:
    """Create token.

    - input:
        - SignInRequest: ding in data
    - output:
        - TokenIssuerResponse: token info
    """
    user_id, token_id, roles = service.get_token_info(
        sess=sess,
        name=content.user,
        password=content.password
    )
    return TokenIssuerResponse(
        exp=1735689600,
        user_id=user_id,
        access_token=AccessTokenResponse(
            aud='greenatom.ru',
            iss='greenatom.ru',
            sub=user_id,
            jti=token_id,
            roles=roles,
            exp=1735689600
        )
    )
