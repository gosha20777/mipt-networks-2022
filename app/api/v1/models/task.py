import uuid
from typing import Any, Dict, Optional, Union

from pydantic import BaseModel
from pydantic.fields import Field

from api.v1.models.common import EngineIdBase
from api.v1.models.enums import TaskStatus


class FaceIdBase(BaseModel):
    face_id: uuid.UUID = Field(
        default=uuid.uuid4(), 
        title='Face Id', 
        description='Face identificator (uuid)',
    )


class FailedResult(BaseModel):
    message: str = Field(
        default='error', 
        title='Error Message', 
        description='Error message'
    )


class FaceRegisterResult(FaceIdBase):
    pass


class FaceQualityResult(BaseModel):
    score: float = Field(
        default=0.8,
        title='Face Quality Score',
        description='Face Quality Score'
    )


class FaceAntiSpoofResult(BaseModel):
    score: float = Field(
        default=0.8, 
        title='Face Anti Spoofing Score', 
        description='Face Anti Spoofing Score'
    )


class FaceMatchResult(BaseModel):
    score: float = Field(
        default=0.8, 
        title='Face Match Score', 
        description='Face Match Score'
    )


class FaceBestMatchResult(FaceMatchResult, FaceIdBase):
    pass


class TaskCreateRequest(EngineIdBase):
    file_hash: str = Field(
        default='8743b52063cd84097a65d1633f5c74f5', 
        title='File Id', 
        description='File identificator (md5)',
        max_length=40
    )


class TaskMatchCreateRequest(TaskCreateRequest, FaceIdBase):
    pass


class TaskResponse(BaseModel):
    status: TaskStatus = Field(
        default=TaskStatus.finished,
        title='Task Status',
        description='Task status in queue'
    )
    result: Optional[
        Union[
            Dict[str, Any],
            FaceRegisterResult,
            FaceQualityResult,
            FaceAntiSpoofResult,
            FaceBestMatchResult,
            FaceMatchResult,
            FailedResult,
        ]
    ] = Field(
        default=FaceRegisterResult(),
        title='Task Result',
        description='Task result',
    )


class TaskCreateResponse(BaseModel):
    task_id: uuid.UUID = Field(
        default=uuid.uuid4(), 
        title='Task Id', 
        description='Task identificator (uuid)',
    )
