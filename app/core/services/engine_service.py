import logging
import uuid
from typing import List, Tuple

from sqlalchemy.orm import Session
from core.provider.manager import ProviderManager

from core.db.operations import engine as db_ops
from core.exceptions.app import InputError

logger = logging.getLogger('engine_service')


def get_engines(
        sess: Session, 
        page: int = 0, 
        limit: int = 50
) -> Tuple[List[uuid.UUID], int]:
    """
    Get engines
    - returns: list of engine IDs, max_page
    """
    if limit <= 0:
        raise InputError('Invalid limit value.')
    db_engines = db_ops.get_engines(
        sess=sess, 
        skip=page * limit, 
        limit=limit
    )
    users = [e.engine_id for e in db_engines]
    count = db_ops.get_engines_count(sess=sess)
    max_page = count // limit
    return users, max_page


def get_engine(
        sess: Session, 
        engine_id: uuid.UUID
) -> Tuple[str, List[uuid.UUID], str, str]:
    """
    Get engine
    - returns: engine_provider, users, description, date
    """
    if len(str(engine_id)) > 36:
        raise InputError('invalid uuid')

    engine = db_ops.get_engine(sess=sess, engine_id=engine_id)
    if engine is None:
        raise InputError('No such engine')

    users = [u.user_id for u in engine.users]
    date = engine.date.date().isoformat()
    return engine.provider, users, engine.description, date
    

def create_engine(
        sess: Session,
        provider_manager: ProviderManager,
        provider: str, 
        description: str = None, 
        users: List[uuid.UUID] = [],
) -> uuid.UUID:
    """
    Create engine
    - returns: engine ID
    """
    if provider not in provider_manager.provider_names:
        raise InputError('no such provider')
    engine = db_ops.create_engine(
        sess=sess, 
        provider=provider, 
        description=description, 
        users=users
    )
    return engine.engine_id
    

def update_engine(
        sess: Session,
        provider_manager: ProviderManager,
        engine_id: str,
        provider: str,
        description: str = None
) -> None:
    '''
    Update engine
    '''
    if provider not in provider_manager.provider_names:
        raise InputError('no such provider')

    if len(str(engine_id)) > 36:
        raise InputError('invalid uuid')

    engine = db_ops.get_engine(
        sess=sess,
        engine_id=engine_id
    )
    if engine is None:
        raise InputError('No such engine to update')

    rows_count = db_ops.update_engine(
        sess=sess,
        engine_id=engine_id,
        provider=provider,
        description=description
    )
    if rows_count != 1:
        logger.warning(f'Update {rows_count} when updating engine')
    

def delete_engine(sess: Session, engine_id: uuid.UUID) -> None:
    """
    Delete engine
    """
    if len(str(engine_id)) > 36:
        raise InputError('invalid uuid')
        
    engine = db_ops.get_engine(
        sess=sess,
        engine_id=engine_id
    )
    if engine is None:
        raise InputError('No such engine to delete')

    rows_count = db_ops.delete_engine(sess=sess, engine_id=engine_id)
    if rows_count != 1:
        logger.warning('Update %s when deleting engine', rows_count)
