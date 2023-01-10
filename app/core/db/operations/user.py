import logging
import uuid
from typing import List, Union

from sqlalchemy.orm import Session

from core.db.models.engine import Engine
from core.db.models.role import Role
from core.db.models.user import User
from core.exceptions.app import InputError
from core.exceptions.db import DbError

logger = logging.getLogger('db')


def create_user(
        sess: Session,
        name: str,
        password: str,
        roles: List[str],
        engines: List[uuid.UUID] = []
) -> User:
    try:
        user = sess.query(User).filter(User.name == name).first()
        if user is not None:
            logger.error("Cann't create user, as such user exists in DB.")
            logger.error(f'User id: {user.user_id}')
            raise ValueError('User with such name exists')

        existing_roles = sess.query(Role).filter(
            Role.role_id.in_(roles)
        ).all()
        if len(existing_roles) != len(roles):
            logger.error("Cann't create user, as some roles are not in DB. ")
            logger.error("Request roles:[%s] DB roles:[%s]" % 
                (
                    ', '.join(roles), 
                    ', '.join([r.role_id for r in existing_roles])
                )
            )
            raise ValueError("Invalid roles")

        existing_engines = sess.query(Engine).filter(
            Engine.engine_id.in_(engines)
        ).all()
        if len(existing_engines) != len(engines):
            logger.error("Cann't create user, as some engines are not in DB. ")
            logger.error("Request engines:[%s] DB engines:[%s]" % 
                (
                    ', '.join([str(e) for e in engines]),
                    ', '.join([e.engine_id for e in existing_engines])
                )
            )
            raise ValueError("Invalid engines")

        user = User(
            user_id=uuid.uuid4(),
            name=name,
            password=password,
            roles=existing_roles,
            engines=existing_engines
        )
        sess.add(user)
        sess.commit()
        sess.refresh(user)
        logger.debug(f'Create user in db: id={user.user_id}')
        return user
    except ValueError as ex:
        raise InputError(str(ex))
    except Exception:
        sess.rollback()
        raise DbError('Can not create user in db')


def update_user(
        sess: Session,
        user_id: uuid.UUID,
        name: str,
        password: str,
        roles: List[str],
        engines: List[uuid.UUID] = []
) -> int:
    try:
        user = sess.query(User).filter(User.user_id == user_id).first()
        if user is None:
            raise ValueError("No such user")

        existing_roles = sess.query(Role).filter(Role.role_id.in_(roles)).all()
        if len(existing_roles) != len(roles):
            logger.error("Cann't update user, as some roles are not in DB. ")
            logger.error("Request roles:[%s] DB roles:[%s]" % 
                (
                    ', '.join([str(e) for e in engines]),
                    ', '.join([r.role_id for r in existing_roles])
                )
            )
            raise ValueError("Invalid roles")

        existing_engines = sess.query(Engine).filter(
            Engine.engine_id.in_(engines)
        ).all()
        if len(existing_engines) != len(engines):
            logger.error("Cann't update user, as some engines are not in DB. ")
            logger.error("Request engines:[%s] DB engines:[%s]" % 
                (
                    ', '.join([str(e) for e in engines]),
                    ', '.join([e.engine_id for e in existing_engines])
                )
            )
            raise ValueError("Invalid engines")

        rows = sess.query(User).filter(
            User.user_id == user_id
        ).update(
            {
                User.name: name,
                User.password: password
            }
        )

        user.roles = existing_roles
        user.engines = existing_engines

        sess.add(user)
        sess.commit()
        sess.refresh(user)

        logger.debug(f'Update user in db: id={user_id}')
        return rows
    except ValueError as ex:
        raise InputError(str(ex))
    except Exception:
        sess.rollback()
        raise DbError('Can not update user in db')


def get_user(sess: Session, user_id: uuid.UUID) -> Union[User, None]:
    try:
        return sess.query(User).filter(
            User.user_id == user_id
        ).first()
    except Exception:
        raise DbError('Can not get user from db')


def get_user_by_name(sess: Session, user_name: str) -> Union[User, None]:
    try:
        return sess.query(User).filter(User.name == user_name).first()
    except Exception:
        raise DbError('Can not get user from db')


def get_users(sess: Session, skip: int = 0, limit: int = 100) -> List[User]:
    try:
        return sess.query(User).offset(skip).limit(limit).all()
    except Exception:
        raise DbError('Can not get users from db')


def get_users_count(sess: Session) -> int:
    try:
        return len(sess.query(User).all())
    except Exception:
        raise DbError('Can not count users in db')


def delete_user(sess: Session, user_id: uuid.UUID) -> int:
    try:
        user = sess.query(User).filter(User.user_id == user_id).first()
        if user is None:
            raise ValueError("No such user")
        user.engines = []
        user.roles = []
        sess.add(user)
        sess.commit()
        sess.refresh(user)

        rows = sess.query(User).filter(User.user_id == user_id).delete()
        sess.commit()
        return rows
    except ValueError as ex:
        raise InputError(str(ex))
    except Exception:
        sess.rollback()
        raise DbError('Can not delete user in db')
