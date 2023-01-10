import logging
import uuid

from fastapi import APIRouter, Query
from fastapi.params import Depends

from api.v1.models.engine import (
    EngineCreateRequest,
    EngineCreateResponse,
    EngineMetadata,
    EngineResponse,
    EnginesResponse,
    EngineUpdateRequest,
    EngineVersion,
)
from core.db.definition import get_db
from core.jwt.token import BearerForm
from core.services import engine_service as service
from core.provider.manager import get_provider_manager

router = APIRouter()
logger = logging.getLogger('engine_api')
db = get_db()
pm = get_provider_manager()


@router.get('/engines', response_model=EnginesResponse)
def get_all_engines(
    page: int = Query(0, le=99999),
    limit: int = Query(50, le=99999),
    sess=Depends(db.get_session),
    _=Depends(BearerForm())
) -> EnginesResponse:
    """Get all engines in the system.

    - input:
        - page: page count
        - limit: number of items in the page
    - output:
        - EnginesResponse: response with engines IDs
    """
    engines, max_page = service.get_engines(sess=sess, page=page, limit=limit)
    return EnginesResponse(
        engines=engines,
        max_page=max_page
    )


@router.post('/engine', response_model=EngineCreateResponse)
def create_engine(
    content: EngineCreateRequest,
    sess=Depends(db.get_session),
    _=Depends(BearerForm())
) -> EngineCreateResponse:
    """Create engine in the system.

    - input:
        - EngineCreateRequest: engine parametrs
    - output:
        - EngineCreateResponse: response with engine ID
    """
    engine_id = service.create_engine(
        sess=sess,
        provider_manager=pm,
        provider=f'{content.engine_type}-{content.version.major}-{content.version.minor}-{content.version.path}',
        description=content.description,
    )
    return EngineCreateResponse(
        engine_id=engine_id
    )


@router.put('/engine')
def update_engine(
    content: EngineUpdateRequest,
    uuid: uuid.UUID = uuid.uuid4(),
    sess=Depends(db.get_session),
    _=Depends(BearerForm())
) -> None:
    """Update engine in the system.

    - input:
        - EngineUpdateRequest: engine parametrs
    """
    service.update_engine(
        sess=sess,
        provider_manager=pm,
        engine_id=uuid,
        provider=f'{content.engine_type}-{content.version.major}-{content.version.minor}-{content.version.path}',
        description=content.description
    )
    return


@router.get('/engine', response_model=EngineResponse)
def get_engine(
    uuid: uuid.UUID = uuid.uuid4(),
    sess=Depends(db.get_session),
    _=Depends(BearerForm())
) -> EngineResponse:
    """Get engine.

    - input:
        - uuid: engine ID
    - output:
        - EngineResponse: engine info
    """
    provider_name, users, description, date = service.get_engine(
        sess=sess, engine_id=uuid
    )
    engine_type, major, minor, path = provider_name.split('-')
    major, minor, path = int(major), int(minor), int(path)
    return EngineResponse(
        engine_type=engine_type,
        users=users,
        description=description,
        date=date,
        version=EngineVersion(major=major, minor=minor, path=path),
        meta_data=EngineMetadata(
            quality_threshold=0.6,
            anti_spoofing_threshold=0.6,
            build='build-0.1.74',
            extra={
                'queue': f'{provider_name}.{uuid}',
                'orchestrator_type': 'thread'
            }
        )
    )
    

@router.delete('/engine')
def delete_engine(
    uuid: uuid.UUID = uuid.uuid4(),
    sess=Depends(db.get_session),
    _=Depends(BearerForm())
) -> None:
    '''
    Delete engine from the system
    - input:
        - uuid: engine ID
    '''
    service.delete_engine(
        sess=sess,
        engine_id=uuid
    )
    return
