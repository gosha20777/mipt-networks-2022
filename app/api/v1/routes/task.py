import logging
import uuid

from fastapi import APIRouter, BackgroundTasks
from fastapi.params import Depends

from api.v1.models.task import (
    TaskCreateRequest,
    TaskCreateResponse,
    TaskMatchCreateRequest,
    TaskResponse,
)
from core.db.definition import get_db
from core.jwt.token import BearerForm
from core.services import task_service as service

router = APIRouter()
logger = logging.getLogger('task_api')
db = get_db()


@router.get('/task', response_model=TaskResponse)
def get_task_result(
        uuid: uuid.UUID = uuid.uuid4(),
        _=Depends(BearerForm())
) -> TaskResponse:
    """Get task result.

    - input:
        - uuid: task ID
    - output:
        - TaskResponse: task info
    """
    result = service.get_task_result(
        task_id=uuid
    )
    return result


@router.post('/task/register', response_model=TaskCreateResponse)
def register_face(
        content: TaskCreateRequest,
        background_tasks: BackgroundTasks,
        sess=Depends(db.get_session),
        _=Depends(BearerForm())
) -> TaskCreateResponse:
    """Register face.

    - input:
        - FaceRequest: task params
    - output:
        - TaskCreateResponse: task id
    """
    task_id = service.register_face(
        sess=sess,
        background_tasks=background_tasks,
        engine_id=content.engine_id,
        file_hash=content.file_hash
    )
    return TaskCreateResponse(
        task_id=task_id
    )


@router.post('/task/quality', response_model=TaskCreateResponse)
def check_face_quality(
        content: TaskCreateRequest,
        background_tasks: BackgroundTasks,
        sess=Depends(db.get_session),
        _=Depends(BearerForm())
) -> TaskCreateResponse:
    """Face quality

    - input:
        - FaceRequest: task params
    - output:
        - TaskCreateResponse: task id
    """
    task_id = service.check_face_quality(
        sess=sess,
        background_tasks=background_tasks,
        engine_id=content.engine_id,
        file_hash=content.file_hash
    )
    return TaskCreateResponse(
        task_id=task_id
    )


@router.post('/task/anti_spoofing', response_model=TaskCreateResponse)
def check_face_anti_spoofing(
        content: TaskCreateRequest,
        background_tasks: BackgroundTasks,
        sess=Depends(db.get_session),
        _=Depends(BearerForm())
) -> TaskCreateResponse:
    """Face anti spoofing

    - input:
        - FaceRequest: task params
    - output:
        - TaskCreateResponse: task id
    """
    task_id = service.check_face_anti_spoofing(
        sess=sess,
        background_tasks=background_tasks,
        engine_id=content.engine_id,
        file_hash=content.file_hash
    )
    return TaskCreateResponse(
        task_id=task_id
    )


@router.post('/task/best_match', response_model=TaskCreateResponse)
def best_match(
        content: TaskCreateRequest,
        background_tasks: BackgroundTasks,
        sess=Depends(db.get_session),
        _=Depends(BearerForm())
) -> TaskCreateResponse:
    """Best match

    - input:
        - FaceRequest: task params
    - output:
        - TaskCreateResponse: task id
    """
    task_id = service.best_match(
        sess=sess,
        background_tasks=background_tasks,
        engine_id=content.engine_id,
        file_hash=content.file_hash
    )
    return TaskCreateResponse(
        task_id=task_id
    )


@router.post("/task/match", response_model=TaskCreateResponse)
def match_with_face(
        content: TaskMatchCreateRequest,
        background_tasks: BackgroundTasks,
        sess=Depends(db.get_session),
        _=Depends(BearerForm())
) -> TaskCreateResponse:
    """
    Match with face
    - input:
        - FaceRequest: task params
    - output:
        - TaskCreateResponse: task id
    """
    task_id = service.match_with_face(
        sess=sess,
        background_tasks=background_tasks,
        engine_id=content.engine_id,
        file_hash=content.file_hash,
        face_id=content.face_id
    )
    return TaskCreateResponse(
        task_id=task_id
    )
