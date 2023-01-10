import logging

from fastapi import APIRouter

from api.v1.models.ping import Pong
from core.config import get_config

router = APIRouter()
logger = logging.getLogger('ping_api')


@router.get('/ping', response_model=Pong)
async def ping() -> Pong:
    project_name = get_config().project_name
    version = get_config().version
    return Pong(pong=f'{project_name}, version {version}')
