from typing import Union

import requests

from core.config import get_config
from core.provider.interfaces import IProvider, IProviderConfig
from core.provider.models.tasks import (
    FaceAntiSpoofResult,
    FaceAntiSpoofTask,
    FaceBestMatchResult,
    FaceBestMatchTask,
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
    base_url: str


class Provider(IProvider):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.__base_url = config.base_url
    
    def register(self, data: bytes) -> Union[FaceRegisterTask, Task]:
        multipart_form_data = {
            'data': ('image', data)
        }
        url = f'{self.__base_url}/register'
        try:
            response = requests.post(
                url, 
                files=multipart_form_data, 
                timeout=get_config().redis_queue_exp
            )
            content = dict(response.json())
        except Exception:
            self._log.error(f'Can not send request to {url}', exc_info=True)
            return Task(
                status=TaskStatus.failed, 
                result=FailedResult(message='Can not send request to engie')
            )
        
        if response.status_code != 200:
            self._log.error(
                f'Get {response.status_code} status code from {url}'
            )
            return Task(
                status=TaskStatus.failed, 
                result=FailedResult(message='Get bad response from engine')
            )
        
        if 'id' not in content.keys():
            self._log.error(f'Get wrong response: {content} from {url}')
            return Task(
                status=TaskStatus.failed, 
                result=FailedResult(message='Get bad response from engine')
            )
        
        user_id = content.get('id')
        if user_id is None:
            self._log.error(f'Get empty user id from {url}')
            return Task(
                status=TaskStatus.failed, 
                result=FailedResult(message='Get bad response from engine')
            )

        return FaceRegisterTask(
            status=TaskStatus.finished,
            result=FaceRegisterResult(face_id=f'{user_id}')
        )

    def quality(self, data: bytes) -> Union[FaceQualityTask, Task]:
        multipart_form_data = {
            'data': ('image', data)
        }
        url = f'{self.__base_url}/quality'
        try:
            response = requests.post(url, files=multipart_form_data)
            content = dict(response.json())
        except Exception:
            self._log.error(
                f'Can not send request to {url}', exc_info=True
            )
            return Task(
                status=TaskStatus.failed, 
                result=FailedResult(message='Can not send request to engie')
            )
        
        if response.status_code != 200:
            self._log.error(
                f'Get {response.status_code} status code from {url}'
            )
            return Task(
                status=TaskStatus.failed, 
                result=FailedResult(message='Get bad response from engine')
            )
        
        if 'score' not in content.keys():
            self._log.error(f'Get wrong response: {content} from {url}')
            return Task(
                status=TaskStatus.failed, 
                result=FailedResult(message='Get bad response from engine')
            )
        
        quality = content.get('score')
        if quality is None:
            self._log.error(f'Get empty quality from {url}')
            return Task(
                status=TaskStatus.failed, 
                result=FailedResult(message='Get bad response from engine')
            )

        return FaceQualityTask(
            status=TaskStatus.finished,
            result=FaceQualityResult(score=float(quality))
        )

    def liveness(self, data: bytes) -> Union[FaceAntiSpoofTask, Task]:
        multipart_form_data = {
            'data': ('image', data)
        }
        url = f'{self.__base_url}/liveness'
        try:
            response = requests.post(url, files=multipart_form_data)
            content = dict(response.json())
        except Exception:
            self._log.error(
                f'Can not send request to {url}', exc_info=True
            )
            return Task(
                status=TaskStatus.failed, 
                result=FailedResult(message='Can not send request to engie')
            )
        
        if response.status_code != 200:
            self._log.error(
                f'Get {response.status_code} status code from {url}'
            )
            return Task(
                status=TaskStatus.failed, 
                result=FailedResult(message='Get bad response from engine')
            )
        
        if 'score' not in content.keys():
            self._log.error(f'Get wrong response: {content} from {url}')
            return Task(
                status=TaskStatus.failed, 
                result=FailedResult(message='Get bad response from engine')
            )
        
        liveness = content.get('score')
        if liveness is None:
            self._log.error(f'Get empty liveness from {url}')
            return Task(
                status=TaskStatus.failed, 
                result=FailedResult(message='Get bad response from engine')
            )

        return FaceAntiSpoofTask(
            status=TaskStatus.finished,
            result=FaceAntiSpoofResult(score=float(liveness))
        )

    def best_match(self, data: bytes) -> Union[FaceBestMatchTask, Task]:
        multipart_form_data = {
            'data': ('image', data)
        }
        url = f'{self.__base_url}/best_batch'
        try:
            response = requests.post(url, files=multipart_form_data)
            content = dict(response.json())
        except Exception:
            self._log.error(f'Can not send request to {url}', exc_info=True)
            return Task(
                status=TaskStatus.failed, 
                result=FailedResult(message='Can not send request to engie')
            )
        
        if response.status_code != 200:
            self._log.error(
                f'Get {response.status_code} status code from {url}'
            )
            return Task(
                status=TaskStatus.failed, 
                result=FailedResult(message='Get bad response from engine')
            )
        
        if 'score' not in content.keys():
            self._log.error(f'Get wrong response: {content} from {url}')
            return Task(
                status=TaskStatus.failed, 
                result=FailedResult(message='Get bad response from engine')
            )
        
        if 'id' not in content.keys():
            self._log.error(f'Get wrong response: {content} from {url}')
            return Task(
                status=TaskStatus.failed, 
                result=FailedResult(message='Get bad response from engine')
            )
        
        score = content.get('score')
        if score is None:
            self._log.error(f'Get empty score from {url}')
            return Task(
                status=TaskStatus.failed, 
                result=FailedResult(message='Get bad response from engine')
            )
        
        user_id = content.get('id')
        if user_id is None:
            self._log.error(f'Get empty uuid from {url}')
            return Task(
                status=TaskStatus.failed, 
                result=FailedResult(message='Get bad response from engine')
            )

        return FaceBestMatchTask(
            status=TaskStatus.finished,
            result=FaceBestMatchResult(
                face_id=f'{user_id}', score=float(score)
            )
        )

    def match_with_face(
            self, 
            data: bytes, 
            internal_id: str
    ) -> Union[FaceMatchTask, Task]:
        self._log.error('Method is not implemented')
        return Task(
            status=TaskStatus.failed, 
            result=FailedResult(message='Method is not implemented')
        )

    def remove_face(self, internal_id: str) -> Task:
        url = f'{self.__base_url}/face'
        try:
            response = requests.delete(url, params={'face_id': internal_id})
        except Exception:
            self._log.error(f'Can not send request to {url}', exc_info=True)
            return Task(
                status=TaskStatus.failed, 
                result=FailedResult(message='Can not send request to engie')
            )

        if response.status_code != 200:
            self._log.error(
                f'Get {response.status_code} status code from {url}'
            )
            return Task(
                status=TaskStatus.failed, 
                result=FailedResult(message='Get bad response from engine')
            )
        
        return Task(
            status=TaskStatus.finished, 
            result=None
        )
