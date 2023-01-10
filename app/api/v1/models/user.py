from typing import List

from pydantic import BaseModel
from pydantic.fields import Field

from api.v1.models.common import (
    DateBase,
    EngineListBase,
    MaxPageBase,
    UserIdBase,
    UserListBase,
    UserNameBase,
)
from api.v1.models.enums import RoleType

# base API


class RoleListBase(BaseModel):
    roles: List[RoleType] = Field(
        default=[RoleType.user, RoleType.admin], 
        title='User roles', 
        description='User roles',
    )


class EngineRoleListBase(EngineListBase, RoleListBase):
    pass


# public API

class UserCreateRequest(UserNameBase, EngineRoleListBase):
    password: str = Field(
        default='password', 
        title='User Password', 
        description='User password',
        max_length=30
    )


class UserUpdateRequest(UserCreateRequest):
    pass


class UserResponse(UserNameBase, DateBase, EngineRoleListBase):
    pass


class UserCreateResponse(UserIdBase):
    pass


class UsersResponse(MaxPageBase, UserListBase):
    pass
