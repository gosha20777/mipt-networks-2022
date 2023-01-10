import logging
import uuid
from typing import List, Union

from sqlalchemy.orm import Session

from core.db.models.descriptor import Descriptor
from core.db.models.engine import Engine
from core.db.models.face import Face
from core.exceptions.db import DbError

logger = logging.getLogger('db')


def create_face(
        sess: Session,
        engine_id: uuid.UUID,
        internal_id: str,
        is_active: bool = True
) -> Face:
    try:
        engine = sess.query(Engine).filter(
            Engine.engine_id == engine_id
        ).first()
        if engine is None:
            logger.error("Cann't create face, as engine are not in DB.")
            logger.error(f"Request engine: {engine_id}")
            raise ValueError("Invalid engine")
        
        descriptor = sess.query(Descriptor).filter(
            Descriptor.descriptor_id == internal_id
        ).first()
        if descriptor is not None:
            logger.error("Cann't create face, as descriptor exists DB.")
            logger.error(f"Descriptor: {internal_id}")
            raise ValueError("Invalid descriptor")
        
        descriptor = Descriptor(
            descriptor_id=internal_id
        )

        face = Face(
            face_id=uuid.uuid4(),
            engine_id=engine_id,
            is_active=is_active,
            engine=engine,
            descriptors=[descriptor]
        )
        sess.add(descriptor)
        sess.add(face)
        sess.commit()
        sess.refresh(descriptor)
        sess.refresh(face)
        logger.debug(f'Create face in db: id={face.face_id}')
        return face
    except Exception as ex:
        sess.rollback()
        raise DbError('Can not create face in db', ex)


def update_face(
        sess: Session,
        face_id: uuid.UUID,
        is_active: bool = True
) -> int:
    try:
        rows = sess.query(Face).filter(Face.face_id == face_id).update(
            {
                Face.is_active: is_active
            }
        )
        sess.commit()
        logger.debug(f'Update face in db: id={face_id}')
        return rows
    except Exception:
        sess.rollback()
        raise DbError('Can not update face in db')


def get_face(sess: Session, face_id: uuid.UUID) -> Union[Face, None]:
    try:
        return sess.query(Face).filter(
            Face.face_id == face_id
        ).first()
    except Exception:
        raise DbError('Can not get face from db')


def get_face_by_internal_id(
        sess: Session, 
        internal_id: str
) -> Union[Face, None]:
    try:
        descriptor = sess.query(Descriptor).filter(
            Descriptor.descriptor_id == internal_id
        ).first()
        return sess.query(Face).filter(
            Face.face_id == descriptor.face_id
        ).first()
    except Exception:
        raise DbError('Can not get face from db')


def get_faces(
        sess: Session, 
        engine_id: uuid.UUID, 
        skip: int = 0, 
        limit: int = 100
) -> List[Face]:
    try:
        return sess.query(Face).filter(
            Face.engine_id == engine_id
        ).offset(skip).limit(limit).all()
    except Exception:
        raise DbError('Can not get faces from db')
    

def get_faces_count(
        sess: Session, 
        engine_id: uuid.UUID
) -> int:
    try:
        return len(
            sess.query(Face).filter(Face.engine_id == engine_id).all()
        )
    except Exception:
        raise DbError('Can not count faces in db')


def delete_face(
        sess: Session, 
        face_id: uuid.UUID
) -> int:
    try:
        face = sess.query(Face).filter(
            Face.face_id == face_id
        ).first()
        if face is None:
            raise ValueError("No such user")
        
        rows = sess.query(Descriptor).filter(
            Descriptor.face_id == face_id
        ).delete()
        # face.descriptors = []
        # sess.add(face)
        # sess.commit()
        # sess.refresh(face)
        rows = sess.query(Face).filter(
            Face.face_id == face_id
        ).delete()
        sess.commit()
        return rows
    except Exception:
        sess.rollback()
        raise DbError('Can not delete face in db')
