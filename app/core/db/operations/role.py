import logging

from sqlalchemy.orm import Session

from core.db.models.role import Role
from core.exceptions.db import DbError

logger = logging.getLogger('db')


def create_role(
        sess: Session,
        role: str,
        description: str = None
) -> Role:
    try:
        role = Role(
            role_id=role,
            description=description
        )
        sess.add(role)
        sess.commit()
        sess.refresh(role)
        logger.debug(f'Create role in db: type={role.role_id}')
        return role
    except Exception:
        sess.rollback()
        raise DbError('Can not create user in db')
