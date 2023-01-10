import uuid
from typing import List

from pydantic.fields import Field

from api.v1.models.common import ExpTtimeBase, UserIdBase, UserNameBase
from api.v1.models.enums import RoleType


class SignInRequest(UserNameBase):
    password: str = Field(
        default='password', 
        title='User Password', 
        description='User password',
        max_length=30
    )


class AccessTokenResponse(ExpTtimeBase):
    aud: str = Field(
        default='greenatom.ru', 
        title='Audience', 
        description='JWT audience'
    )
    iss: str = Field(
        default='greenatom.ru', 
        title='Issuer', 
        description='JWT Issuer'
    )
    sub: uuid.UUID = Field(
        default=uuid.uuid4(), 
        title='Subject', 
        description='JWT Subject (user id)'
    )
    jti: uuid.UUID = Field(
        default=uuid.uuid4(), 
        title='JWT ID', 
        description='JWT ID (sessin id)',
    )
    roles: List[RoleType] = Field(
        default=[RoleType.user, RoleType.admin], 
        title='User roles', 
        description='User roles',
    )


class TokenIssuerResponse(UserIdBase, ExpTtimeBase):
    exp: int = Field(
        default=1735689600,
        title='Expired Time',
        description='expired time in unix time format',
    )
    access_token: AccessTokenResponse = Field(
        title='Access Token', 
        description='Access JWT token'
    )


class TokenResponse(UserIdBase, ExpTtimeBase):
    access_token: str = Field(
        default='x.y.z',
        title='Access Token', 
        description='Access JWT token'
    )
