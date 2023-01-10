import logging
import pickle
import uuid

from fastapi import BackgroundTasks
from redis import Redis
from sqlalchemy.orm import Session

from core import orchestrator
from core.config import get_config
from core.db.operations import engine as db_ops
from core.exceptions.app import AppError, InputError
from core.provider.manager import get_provider_manager
from core.provider.models.enums import TaskStatus
from core.provider.models.tasks import BaseTask, Task

logger = logging.getLogger('user_service')
redis_tasks = Redis(
    host=get_config().redis_host,
    port=get_config().redis_port, 
    db=get_config().redis_queue_db
)
redis_cashe = Redis(
    host=get_config().redis_host,
    port=get_config().redis_port, 
    db=get_config().redis_cashe_db
)
pm = get_provider_manager()


def get_task_result(task_id: uuid.UUID) -> BaseTask:
    if len(str(task_id)) > 36:
        raise InputError('invalid uuid')
    try:
        raw_result = redis_tasks.get(name=str(task_id))
    except Exception:
        logger.error('Can not get result from redis.', exc_info=True)
        raise AppError('Can not get result from redis.')
    if raw_result is None:
        raise InputError('No such task')

    result = pickle.loads(raw_result)
    if not isinstance(result, BaseTask):
        logger.error('Invalid result type: %s but %s', BaseTask, type(result))
        raise AppError('Invalid result type')
    return result


def register_face(
        sess: Session,
        background_tasks: BackgroundTasks,
        engine_id: uuid.UUID,
        file_hash: str
) -> uuid.UUID:
    if len(str(engine_id)) > 36:
        raise InputError('invalid uuid')

    engine = db_ops.get_engine(sess=sess, engine_id=engine_id)
    if engine is None:
        raise InputError('No such engine')
        
    try:
        raw_file = redis_cashe.get(name=file_hash)
    except Exception:
        logger.error('Can not get file from redis.', exc_info=True)
        raise AppError('Can not get file from redis.')

    if raw_file is None:
        raise InputError('No such file')
        
    if engine.provider not in pm.provider_names:
        raise InputError('No such provider')

    task_id = uuid.uuid4()
    task_id_in_redis = str(task_id)

    try:
        redis_tasks.set(
            name=task_id_in_redis,
            value=pickle.dumps(Task(status=TaskStatus.queued)),
            ex=get_config().redis_queue_exp,
        )
    except Exception:
        logger.error('Can not set task in redis.', exc_info=True)
        raise AppError('Can not set task in redis.')
    background_tasks.add_task(
        orchestrator.register_face,
        task_id=task_id_in_redis,
        engine_id=engine_id,
        provider=pm.get_provider(engine.provider),
        data=raw_file,
        redis=redis_tasks,
        sess=sess
    )
    return task_id


def check_face_quality(
        sess: Session,
        background_tasks: BackgroundTasks,
        engine_id: uuid.UUID,
        file_hash: str
) -> uuid.UUID:
    if len(str(engine_id)) > 36:
        raise InputError('invalid uuid')

    engine = db_ops.get_engine(sess=sess, engine_id=engine_id)
    if engine is None:
        raise InputError('No such engine')

    try:
        raw_file = redis_cashe.get(name=file_hash)
    except Exception:
        logger.error('Can not get file from redis.', exc_info=True)
        raise AppError('Can not get file from redis.')
        
    if raw_file is None:
        raise InputError('No such file')

    if engine.provider not in pm.provider_names:
        raise InputError('No such provider')

    task_id = uuid.uuid4()
    task_id_in_redis = str(task_id)

    try:
        redis_tasks.set(
            name=task_id_in_redis,
            value=pickle.dumps(Task(status=TaskStatus.queued)),
            ex=get_config().redis_queue_exp,
        )
    except Exception:
        logger.error('Can not set task in redis.', exc_info=True)
        raise AppError('Can not set task in redis.')

    background_tasks.add_task(
        orchestrator.face_quality,
        task_id=task_id_in_redis,
        provider=pm.get_provider(engine.provider),
        data=raw_file,
        redis=redis_tasks,
    )
    return task_id


def check_face_anti_spoofing(
        sess: Session,
        background_tasks: BackgroundTasks,
        engine_id: uuid.UUID,
        file_hash: str
) -> uuid.UUID:
    if len(str(engine_id)) > 36:
        raise InputError('invalid uuid')

    engine = db_ops.get_engine(sess=sess, engine_id=engine_id)
    if engine is None:
        raise InputError('No such engine')
        
    try:
        raw_file = redis_cashe.get(name=file_hash)
    except Exception:
        logger.error('Can not get file from redis.', exc_info=True)
        raise AppError('Can not get file from redis.')

    if raw_file is None:
        raise InputError('No such file')
        
    if engine.provider not in pm.provider_names:
        raise InputError('No such provider')

    task_id = uuid.uuid4()
    task_id_in_redis = str(task_id)

    try:
        redis_tasks.set(
            name=task_id_in_redis,
            value=pickle.dumps(Task(status=TaskStatus.queued)),
            ex=get_config().redis_queue_exp,
        )
    except Exception:
        logger.error('Can not set task in redis.', exc_info=True)
        raise AppError('Can not set task in redis.')

    background_tasks.add_task(
        orchestrator.face_liveness,
        task_id=task_id_in_redis,
        provider=pm.get_provider(engine.provider),
        data=raw_file,
        redis=redis_tasks,
    )
    return task_id


def best_match(
        sess: Session,
        background_tasks: BackgroundTasks,
        engine_id: uuid.UUID,
        file_hash: str
) -> uuid.UUID:
    if len(str(engine_id)) > 36:
        raise InputError('invalid uuid')

    engine = db_ops.get_engine(sess=sess, engine_id=engine_id)
    if engine is None:
        raise InputError('No such engine')
        
    try:
        raw_file = redis_cashe.get(name=file_hash)
    except Exception:
        logger.error('Can not get file from redis.', exc_info=True)
        raise AppError('Can not get file from redis.')

    if raw_file is None:
        raise InputError('No such file')
        
    if engine.provider not in pm.provider_names:
        raise InputError('No such provider')

    task_id = uuid.uuid4()
    task_id_in_redis = str(task_id)

    try:
        redis_tasks.set(
            name=task_id_in_redis,
            value=pickle.dumps(Task(status=TaskStatus.queued)),
            ex=get_config().redis_queue_exp,
        )
    except Exception:
        logger.error('Can not set task in redis.', exc_info=True)
        raise AppError('Can not set task in redis.')

    background_tasks.add_task(
        orchestrator.best_match,
        task_id=task_id_in_redis,
        provider=pm.get_provider(engine.provider),
        data=raw_file,
        redis=redis_tasks,
        sess=sess
    )
    return task_id


def match_with_face(
        sess: Session,
        background_tasks: BackgroundTasks,
        engine_id: uuid.UUID,
        file_hash: str,
        face_id: uuid.UUID
) -> uuid.UUID:
    if len(str(engine_id)) > 36:
        raise InputError('invalid uuid')

    engine = db_ops.get_engine(sess=sess, engine_id=engine_id)
    if engine is None:
        raise InputError('No such engine')

    try:
        raw_file = redis_cashe.get(name=file_hash)
    except Exception:
        logger.error('Can not get file from redis.', exc_info=True)
        raise AppError('Can not get file from redis.')

    if raw_file is None:
        raise InputError('No such file')

    if engine.provider not in pm.provider_names:
        raise InputError('No such provider')

    task_id = uuid.uuid4()
    task_id_in_redis = str(task_id)

    try:
        redis_tasks.set(
            name=task_id_in_redis,
            value=pickle.dumps(Task(status=TaskStatus.queued)),
            ex=get_config().redis_queue_exp,
        )
    except Exception:
        logger.error('Can not set task in redis.', exc_info=True)
        raise AppError('Can not set task in redis.')

    background_tasks.add_task(
        orchestrator.match_with_face,
        task_id=task_id_in_redis,
        provider=pm.get_provider(engine.provider),
        data=raw_file,
        face_id=face_id,
        redis=redis_tasks,
        sess=sess
    )
    return task_id
