import hashlib
import logging
import re
import uuid
from typing import List, Tuple

from sqlalchemy.orm import Session

from core.db.operations import user as db_ops
from core.exceptions.app import InputError

logger = logging.getLogger('user_service')


def get_users(
        sess: Session,
        page: int = 0, 
        limit: int = 50
) -> Tuple[List[uuid.UUID], int]:
    """
    Get users
    - returns: list of user IDs, max_page
    """
    if limit <= 0:
        raise InputError('Invalid limit value.')
    db_users = db_ops.get_users(sess=sess, skip=page * limit, limit=limit)
    users = [u.user_id for u in db_users]
    count = db_ops.get_users_count(sess=sess)
    max_page = count // limit
    return users, max_page
    

def get_user(
        sess: Session, 
        user_id: uuid.UUID
) -> Tuple[str, List[uuid.UUID], List[str], str]:
    """
    Get user
    - returns: user name, list of engines IDs, list of roles, date
    """
    if len(str(user_id)) > 36:
        raise InputError('invalid uuid')

    user = db_ops.get_user(sess=sess, user_id=user_id)
    if user is None:
        raise InputError('No such user')

    engines = [e.engine_id for e in user.engines]
    roles = [r.role_id for r in user.roles]
    date = user.date.date().isoformat()
    return user.name, engines, roles, date


def create_user(
        sess: Session,
        name: str,
        password: str,
        roles: List[str],
        engines: List[uuid.UUID] = []
) -> uuid.UUID:
    """
    Create user
    - returns: user ID
    """
    if re.match(r'^[a-zA-Z0-9_\-]{3,20}$', name) is None:
        raise InputError('Invalid user name')

    if len(password) < 6:
        raise InputError('Password too short')

    user = db_ops.create_user(
        sess=sess,
        name=name,
        password=hashlib.md5(password.encode()).hexdigest(),
        roles=roles,
        engines=engines
    )
    return user.user_id
    

def update_user(
        sess: Session,
        user_id: uuid.UUID,
        name: str,
        password: str,
        roles: List[str],
        engines: List[uuid.UUID] = []
) -> None:
    """
    Update user
    """
    if len(str(user_id)) > 36:
        raise InputError('invalid uuid')

    if re.match(r'^[a-zA-Z0-9_\-]{3,20}$', name) is None:
        raise InputError('Invalid user name')

    if len(password) < 6:
        raise InputError('Password too short')

    user = db_ops.get_user(
        sess=sess,
        user_id=user_id
    )
    if user is None:
        raise InputError('No such user to update')

    roles_map = {
        'user': 0,
        'admin': 1,
        'root': 2
    }

    max_current_role = max([roles_map.get(r.role_id) for r in user.roles])
    max_new_role = max([roles_map.get(r.role_id) for r in roles])
    if max_new_role > max_current_role:
        raise InputError('Cannot assign higher role')
    
    rows_count = db_ops.update_user(
        sess=sess,
        user_id=user_id,
        name=name,
        password=hashlib.md5(password.encode()).hexdigest(),
        roles=roles,
        engines=engines
    )
    if rows_count != 1:
        logger.warning(f'Update {rows_count} when updating user')


def delete_user(sess: Session, user_id: uuid.UUID) -> None:
    """
    Delete user
    """
    if len(str(user_id)) > 36:
        raise InputError('invalid uuid')
        
    user = db_ops.get_user(
        sess=sess,
        user_id=user_id
    )
    if user is None:
        raise InputError('No such user to delete')
    
    rows_count = db_ops.delete_user(sess=sess, user_id=user_id)
    if rows_count != 1:
        logger.warning('Update %s when deleting user', rows_count)
