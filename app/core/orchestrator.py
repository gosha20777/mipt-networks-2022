import logging
import pickle
import uuid
from typing import List, Union

from redis import Redis
from sqlalchemy.orm import Session

from core.config import get_config
from core.db.operations import face as db_ops
from core.provider.interfaces import IProvider
from core.provider.models.tasks import (
    FaceMatchResult,
    FaceMatchTask,
    FailedResult,
    Task,
    TaskStatus,
)

logger = logging.getLogger('orchestartor')


def register_face(
        task_id: str,
        engine_id: uuid.UUID,
        provider: IProvider, 
        data: bytes, 
        redis: Redis,
        sess: Session
) -> None:
    redis.set(
        name=task_id,
        value=pickle.dumps(Task(status=TaskStatus.started)),
        ex=get_config().redis_queue_exp,
    )
    logger.info('start task %s', task_id)

    try:
        result = provider.register(data=data)

        if result.status == TaskStatus.finished:
            internal_id = provider.name + str(result.result.face_id)
            face = db_ops.create_face(
                sess=sess, 
                engine_id=engine_id,
                internal_id=internal_id
            )
            result.result.face_id = face.face_id

        redis.set(
            name=task_id,
            value=pickle.dumps(result),
            ex=get_config().redis_queue_exp,
        )
        logger.info('finish task %s', task_id)
    except Exception:
        redis.set(
            name=task_id,
            value=pickle.dumps(
                Task(
                    status=TaskStatus.failed,
                    result=FailedResult(message='Internal provider error'),
                ),
            ),
            ex=get_config().redis_queue_exp,
        )
        logging.error('Internal provider error', exc_info=True)


def face_quality(
        task_id: str, 
        provider: IProvider, 
        data: bytes, redis: Redis
) -> None:
    redis.set(
        name=task_id,
        value=pickle.dumps(Task(status=TaskStatus.started)),
        ex=get_config().redis_queue_exp,
    )
    logger.info('start task %s', task_id)

    try:
        result = provider.quality(data=data)
        redis.set(
            name=task_id,
            value=pickle.dumps(result),
            ex=get_config().redis_queue_exp,
        )
        logger.info('finish task %s', task_id)
    except Exception:
        redis.set(
            name=task_id,
            value=pickle.dumps(
                Task(
                    status=TaskStatus.failed,
                    result=FailedResult(message='Internal provider error'),
                ),
            ),
            ex=get_config().redis_queue_exp,
        )
        logging.error('Internal provider error', exc_info=True)


def face_liveness(
        task_id: str, 
        provider: IProvider, 
        data: bytes, redis: Redis
) -> None:
    redis.set(
        name=task_id,
        value=pickle.dumps(Task(status=TaskStatus.started)),
        ex=get_config().redis_queue_exp,
    )
    logger.info('start task %s', task_id)

    try:
        result = provider.liveness(data=data)
        redis.set(
            name=task_id,
            value=pickle.dumps(result),
            ex=get_config().redis_queue_exp,
        )
        logger.info('finish task %s', task_id)
    except Exception:
        redis.set(
            name=task_id,
            value=pickle.dumps(
                Task(
                    status=TaskStatus.failed,
                    result=FailedResult(message='Internal provider error'),
                ),
            ),
            ex=get_config().redis_queue_exp,
        )
        logging.error('Internal provider error', exc_info=True)


def best_match(
        task_id: str, 
        provider: IProvider, 
        data: bytes, 
        redis: Redis,
        sess: Session
) -> None:
    redis.set(
        name=task_id,
        value=pickle.dumps(Task(status=TaskStatus.started)),
        ex=get_config().redis_queue_exp,
    )
    logger.info('start task %s', task_id)

    try:
        result = provider.best_match(data=data)

        if result.status == TaskStatus.finished:
            internal_id = provider.name + str(result.result.face_id)
            face = db_ops.get_face_by_internal_id(
                sess=sess,
                internal_id=internal_id
            )
            if face is None:
                raise Exception('No face in db')

            result.result.face_id = face.face_id

        redis.set(
            name=task_id,
            value=pickle.dumps(result),
            ex=get_config().redis_queue_exp,
        )
        logger.info('finish task %s', task_id)
    except Exception:
        redis.set(
            name=task_id,
            value=pickle.dumps(
                Task(
                    status=TaskStatus.failed,
                    result=FailedResult(message='Internal provider error'),
                ),
            ),
            ex=get_config().redis_queue_exp,
        )
        logging.error('Internal provider error', exc_info=True)


def match_with_face(
        task_id: str, 
        provider: IProvider, 
        data: bytes, 
        face_id: uuid.UUID, 
        redis: Redis,
        sess: Session
) -> None:
    redis.set(
        name=task_id,
        value=pickle.dumps(Task(status=TaskStatus.started)),
        ex=get_config().redis_queue_exp,
    )
    logger.info('start task %s', task_id)

    try:
        face = db_ops.get_face(sess=sess, face_id=face_id)
        if face is None:
            raise Exception('No sush face')
        
        if face.descriptors is None or len(face.descriptors) == 0:
            raise Exception('No descriptors in face')
        
        results = []
        for descriptor in face.descriptors:
            internal_id = str(
                descriptor.descriptor_id
            ).replace(provider.name, '')
            
            res = provider.match_with_face(
                data=data, 
                internal_id=internal_id
            )
            results.append(res)

        result = __get_match_result(results=results)
        
        redis.set(
            name=task_id, 
            value=pickle.dumps(result), 
            ex=get_config().redis_queue_exp
        )
        logger.info('finish task %s', task_id)
    except Exception:
        redis.set(
            name=task_id,
            value=pickle.dumps(
                Task(
                    status=TaskStatus.failed,
                    result=FailedResult(message='Internal provider error'),
                ),
            ),
            ex=get_config().redis_queue_exp,
        )
        logging.error('Internal provider error', exc_info=True)


def __get_match_result(
        results: List[Union[Task, FaceMatchTask]]
) -> Union[Task, FaceMatchTask]:
    scores = []

    for res in results:
        if res.status == TaskStatus.finished:
            scores.append(res.result.score)
    
    if len(scores) == 0:
        return results[0]
    return FaceMatchTask(
        status=TaskStatus.finished,
        result=FaceMatchResult(score=max(scores))
    )
