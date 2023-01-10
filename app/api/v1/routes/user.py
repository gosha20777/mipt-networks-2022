import logging
import uuid

from fastapi import APIRouter, Query
from fastapi.params import Depends

from api.v1.models.user import (
    UserCreateRequest,
    UserCreateResponse,
    UserResponse,
    UsersResponse,
    UserUpdateRequest,
)
from core.db.definition import get_db
from core.jwt.token import BearerForm
from core.services import user_service as service

router = APIRouter()
logger = logging.getLogger('user_api')
db = get_db()


@router.get('/users', response_model=UsersResponse)
def get_all_users(
        page: int = Query(0, le=99999),
        limit: int = Query(50, le=99999),
        sess=Depends(db.get_session),
        _=Depends(BearerForm())
) -> UsersResponse:
    """Get all users in the system.

    - input:
        - page: page count
        - limit: number of items in the page
    - output:
        - UsersResponse: response with users
    """
    users, max_page = service.get_users(sess=sess, page=page, limit=limit)
    return UsersResponse(
        users=users,
        max_page=max_page
    )


@router.post('/user', response_model=UserCreateResponse)
def create_user(
        content: UserCreateRequest,
        sess=Depends(db.get_session)
) -> UserCreateResponse:
    """Create user in the system.

    - input:
        - UserCreateRequest: user parametrs
    - output:
        - UserCreateResponse: response with user ID
    """
    user_id = service.create_user(
        sess=sess,
        name=content.user,
        password=content.password,
        roles=content.roles,
        engines=content.engines
    )
    return UserCreateResponse(
        user_id=user_id
    )


@router.put('/user')
def update_user(
    content: UserUpdateRequest,
    uuid: uuid.UUID = uuid.uuid4(),
    sess=Depends(db.get_session),
    _=Depends(BearerForm())
) -> None:
    """Update user in the system.

    - input:
        - UserUpdateRequest: user parametrs
    """
    service.update_user(
        sess=sess,
        user_id=uuid,
        name=content.user,
        password=content.password,
        roles=content.roles,
        engines=content.engines
    )
    return


@router.get("/user", response_model=UserResponse)
def get_user(
    uuid: uuid.UUID = uuid.uuid4(),
    sess=Depends(db.get_session),
    _=Depends(BearerForm())
) -> UserResponse:
    """Get user.

    - input:
        - uuid: user ID
    - output:
        - UserResponse: user info
    """
    name, engines, roles, date = service.get_user(
        sess=sess,
        user_id=uuid
    )
    return UserResponse(
        user=name,
        engines=engines,
        roles=roles,
        date=date
    )


@router.delete('/user')
def delete_user(
    uuid: uuid.UUID = uuid.uuid4(),
    sess=Depends(db.get_session),
    _=Depends(BearerForm())
) -> None:
    """Delete user from the system.

    - input:
        - uuid: user ID
    """
    service.delete_user(
        sess=sess,
        user_id=uuid
    )
    return
