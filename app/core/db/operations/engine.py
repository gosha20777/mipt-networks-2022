import logging
import uuid
from typing import List, Union

from sqlalchemy.orm import Session

from core.db.models.engine import Engine
from core.db.models.face import Face
from core.db.models.user import User
from core.exceptions.app import InputError
from core.exceptions.db import DbError

logger = logging.getLogger('db')


def create_engine(
        sess: Session,
        provider: str,
        description: str = None,
        users: List[uuid.UUID] = []
) -> Engine:
    try:
        existing_users = sess.query(User).filter(
            User.user_id.in_(users)
        ).all()
        if len(existing_users) != len(users):
            logger.error("Cann't create engine, as some users are not in DB.")
            logger.error("Request users:[%s] DB users:[%s]" %
                (
                    ', '.join([str(u) for u in users]),
                    ', '.join([u.user_id for u in existing_users])
                )
            )
            raise ValueError("Invalid users")

        engine = Engine(
            engine_id=uuid.uuid4(),
            provider=provider,
            description=description,
            users=existing_users
        )
        sess.add(engine)
        sess.commit()
        sess.refresh(engine)
        logger.debug(f'Create engine in db: id={engine.engine_id}')
        return engine
    except ValueError as ex:
        raise InputError(str(ex))
    except Exception:
        sess.rollback()
        raise DbError('Can not create engine in db')


def update_engine(
        sess: Session,
        engine_id: uuid.UUID,
        provider: str,
        description: str = None
) -> int:
    try:
        engine = sess.query(Engine).filter(
            Engine.engine_id == engine_id
        ).first()
        if engine is None:
            raise ValueError("No such engine")

        rows = sess.query(Engine).filter(
            Engine.engine_id == engine_id
        ).update(
            {
                Engine.provider: provider,
                Engine.description: description,
            }
        )
        sess.commit()
        logger.debug(f'Update engine in db: id={engine_id}')
        return rows
    except Exception:
        sess.rollback()
        raise DbError('Can not create engine in db')


def get_engine(
        sess: Session, 
        engine_id: uuid.UUID
) -> Union[Engine, None]:
    return sess.query(Engine).filter(Engine.engine_id == engine_id).first()


def get_engines(
        sess: Session, 
        skip: int = 0, 
        limit: int = 100
) -> List[Engine]:
    try:
        return sess.query(Engine).offset(skip).limit(limit).all()
    except Exception:
        raise DbError('Can not get engines from db')


def get_engines_count(sess: Session) -> int:
    try:
        return len(sess.query(Engine).all())
    except Exception:
        raise DbError('Can not get engines from db')


def delete_engine(sess: Session, engine_id: uuid.UUID) -> int:
    try:
        engine = sess.query(Engine).filter(
            Engine.engine_id == engine_id
        ).first()
        if engine is None:
            raise ValueError("No such engine")
        engine.users = []
        engine.faces = []
        sess.add(engine)
        sess.commit()
        sess.refresh(engine)

        rows = sess.query(Engine).filter(
            Engine.engine_id == engine_id
        ).delete()
        sess.query(Face).filter(Face.engine_id == engine_id).delete()
        sess.commit()
        return rows
    except ValueError as ex:
        raise InputError(str(ex))
    except Exception:
        sess.rollback()
        raise DbError('Can not delete user in db')
