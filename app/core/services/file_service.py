import hashlib
import logging
from typing import Tuple

from redis import Redis

from core.config import get_config
from core.exceptions.app import AppError, InputError
from core.provider.models.enums import FileStatus

logger = logging.getLogger('file_service')
redis_cashe = Redis(
    host=get_config().redis_host,
    port=get_config().redis_port,
    db=get_config().redis_cashe_db
)


def upload_file(data: bytes) -> Tuple[str, int]:
    hash_str = hashlib.md5(data).hexdigest()
    try:
        redis_cashe.set(
            name=hash_str, 
            value=data, 
            ex=get_config().redis_cashe_exp
        )
    except Exception:
        logger.error('Can not save file in Redis db', exc_info=True)
        raise AppError('Can not save file')
    return hash_str, get_config().redis_cashe_exp


def get_file_status(file_hash: str) -> FileStatus:
    try:
        data = redis_cashe.get(file_hash)
    except Exception:
        logger.error('Can not get file from Redis db', exc_info=True)
        raise AppError('Can not get file')
    if data is None:
        return FileStatus.not_found
    return FileStatus.available


def get_file(file_hash: str) -> bytes:
    try:
        data = redis_cashe.get(file_hash)
    except Exception:
        logger.error('Can not get file from Redis db', exc_info=True)
        raise AppError('Can not get file')
    if data is None:
        raise InputError('No such file')
    return data
