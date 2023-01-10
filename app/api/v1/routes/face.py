import logging
import uuid

from fastapi import APIRouter, Query
from fastapi.params import Depends

from api.v1.models.face import FaceResponse, FacesResponse
from core.db.definition import get_db
from core.jwt.token import BearerForm
from core.services import face_service as service

router = APIRouter()
logger = logging.getLogger('face_api')
db = get_db()


@router.get('/faces', response_model=FacesResponse)
async def get_all_faces(
        page: int = Query(0, le=99999), 
        limit: int = Query(50, le=99999), 
        engine_id: uuid.UUID = uuid.uuid4(),
        sess=Depends(db.get_session),
        _=Depends(BearerForm())
) -> FacesResponse:
    """Get all faces in the engine.

    - input:
        - page: page count
        - limit: number of items in the page
        - engine_id: engine UUID
    - output:
        - FacesResponse: response with faces
    """
    faces, max_page = service.get_faces(
        sess=sess,
        engine_id=engine_id,
        page=page, 
        limit=limit
    )
    return FacesResponse(
        faces=faces,
        max_page=max_page
    )
    

@router.get('/face')
async def get_face(
        uuid: uuid.UUID = uuid.uuid4(),
        sess=Depends(db.get_session),
        _=Depends(BearerForm())
) -> FaceResponse:
    """Get face.

    - input:
        - uuid: face ID
    - output:
        - FaceResponse: face info
    """
    engine_id, is_active, descriptors = service.get_face(
        sess=sess,
        face_id=uuid
    )
    return FaceResponse(
        engine_id=engine_id,
        is_active=is_active,
        descriptors=descriptors
    )


@router.delete('/face')
async def remove_face(
        uuid: uuid.UUID = uuid.uuid4(),
        sess=Depends(db.get_session),
        _=Depends(BearerForm())
) -> FaceResponse:
    """Remove face.

    - input:
        - uuid: face ID
    """
    service.remove_face(
        sess=sess,
        face_id=uuid
    )
    return
