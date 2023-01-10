import hashlib
import logging
import uuid
from typing import List, Tuple

from sqlalchemy.orm import Session

from core.db.operations import user as db_ops
from core.exceptions.app import InputError

logger = logging.getLogger('user_service')


def get_token_info(
        sess: Session, 
        name: str, 
        password: str
) -> Tuple[uuid.UUID, uuid.UUID, List[str]]:
    """
    Get user
    - returns: user ID, token ID, list of roles
    """
    user = db_ops.get_user_by_name(sess=sess, user_name=name)
    if user is None:
        raise InputError('No such user')
    
    if hashlib.md5(password.encode()).hexdigest() != user.password:
        raise InputError('Incorrect password')
    
    user_id = user.user_id
    roles = [r.role_id for r in user.roles]
    token_id = uuid.uuid4()
    return user_id, token_id, roles
