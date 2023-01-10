import logging
import uuid
from typing import List, Tuple

from sqlalchemy.orm import Session

from core.db.operations import face as db_ops
from core.exceptions.app import AppError, InputError
from core.provider.manager import get_provider_manager
from core.provider.models.enums import TaskStatus

logger = logging.getLogger('user_service')
pm = get_provider_manager()


def get_faces(
        sess: Session,
        engine_id: uuid.UUID,
        page: int = 0, 
        limit: int = 50,
) -> Tuple[List[uuid.UUID], int]:
    """
    Get faces
    - returns: list of face IDs, max_page
    """
    if len(str(engine_id)) > 36:
        raise InputError('invalid uuid')

    if limit <= 0:
        raise InputError('Invalid limit value.')
    db_faces = db_ops.get_faces(
        sess=sess, 
        engine_id=engine_id, 
        skip=page * limit, 
        limit=limit
    )
    faces = [f.face_id for f in db_faces]
    count = db_ops.get_faces_count(sess=sess, engine_id=engine_id)
    max_page = count // limit
    return faces, max_page
    

def get_face(
        sess: Session, 
        face_id: uuid.UUID
) -> Tuple[uuid.UUID, bool, List[str]]:
    """
    Get face
    - returns: engine ID, is active, list of descriptors
    """
    if len(str(face_id)) > 36:
        raise InputError('invalid uuid')

    face = db_ops.get_face(sess=sess, face_id=face_id)
    if face is None:
        raise InputError('No such face')

    engine_id = face.engine_id
    descriptors = [d.descriptor_id for d in face.descriptors]
    is_active = face.is_active
    return engine_id, is_active, descriptors


def remove_face(
        sess: Session, 
        face_id: uuid.UUID,
) -> None:
    """
    Remove face
    """
    if len(str(face_id)) > 36:
        raise InputError('invalid uuid')

    face = db_ops.get_face(sess=sess, face_id=face_id)
    if face is None:
        raise InputError('No such face')

    engine = face.engine
    if engine.provider not in pm.provider_names:
        raise InputError('No such provider')
    
    provider = pm.get_provider(engine.provider)
    for descriptor in face.descriptors:
        internal_id = str(
            descriptor.descriptor_id
        ).replace(provider.name, '')
        task = provider.remove_face(internal_id=internal_id)
        if task.status != TaskStatus.finished:
            raise AppError(f'Can not delete face {face_id}')
    
    db_ops.delete_face(sess=sess, face_id=face_id)
