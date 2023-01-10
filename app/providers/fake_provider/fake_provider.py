import uuid
from time import sleep
from typing import Union

from core.provider.interfaces import IProvider, IProviderConfig
from core.provider.models.tasks import (
    FaceAntiSpoofResult,
    FaceAntiSpoofTask,
    FaceBestMatchResult,
    FaceBestMatchTask,
    FaceMatchResult,
    FaceMatchTask,
    FaceQualityResult,
    FaceQualityTask,
    FaceRegisterResult,
    FaceRegisterTask,
    FailedResult,
    Task,
    TaskStatus,
)


class Config(IProviderConfig):
    my_param: str


class Provider(IProvider):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.__my_param = config.my_param
        self.db = []
    
    def register(self, data: bytes) -> Union[FaceRegisterTask, Task]:
        self._log.info('sleep...')
        sleep(2)
        self.db.append(uuid.uuid4())
        self._log.info('register face')
        return FaceRegisterTask(
            status=TaskStatus.finished,
            result=FaceRegisterResult(face_id=f'{self.db[-1]}')
        )

    def quality(self, data: bytes) -> Union[FaceQualityTask, Task]:
        sleep(2)
        self._log.info('face quality')
        return FaceQualityTask(
            status=TaskStatus.finished,
            result=FaceQualityResult(score=0.9)
        )

    def liveness(self, data: bytes) -> Union[FaceAntiSpoofTask, Task]:
        sleep(2)
        self._log.info('face anti spoofing')
        return FaceAntiSpoofTask(
            status=TaskStatus.finished,
            result=FaceAntiSpoofResult(score=0.9)
        )

    def best_match(self, data: bytes) -> Union[FaceBestMatchTask, Task]:
        sleep(2)
        if len(self.db) == 0:
            return Task(
                status=TaskStatus.failed,
                result=FailedResult(
                    message='No faces in db'
                )
            )

        self._log.info('best match')
        return FaceBestMatchTask(
            status=TaskStatus.finished,
            result=FaceBestMatchResult(face_id=f'{self.db[-1]}', score=0.9)
        )

    def match_with_face(
            self, 
            data: bytes, 
            internal_id: str
    ) -> Union[FaceMatchTask, Task]:
        sleep(2)
        self._log.info('match with face')
        return FaceMatchTask(
            status=TaskStatus.finished,
            result=FaceMatchResult(score=0.9)
        )

    def remove_face(self, internal_id: str) -> Task:
        sleep(2)
        self._log.info('remove face')
        return Task(
            status=TaskStatus.finished
        )
