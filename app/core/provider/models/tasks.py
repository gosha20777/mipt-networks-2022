from typing import Optional, Union

from pydantic import BaseModel

from core.provider.models.enums import TaskStatus


class FailedResult(BaseModel):
    message: str

    def __init__(self, message: str) -> None:
        super().__init__(message=message)


class FaceRegisterResult(BaseModel):
    face_id: str

    def __init__(self, face_id: str) -> None:
        super().__init__(face_id=face_id)


class FaceQualityResult(BaseModel):
    score: float

    def __init__(self, score: float) -> None:
        super().__init__(score=score)


class FaceAntiSpoofResult(FaceQualityResult):
    pass


class FaceMatchResult(FaceQualityResult):
    pass


class FaceBestMatchResult(BaseModel):
    face_id: str
    score: float

    def __init__(
            self, 
            score: float, 
            face_id: str
    ) -> None:
        super().__init__(score=score, face_id=face_id)


class BaseTask(BaseModel):
    status: TaskStatus
    result: Optional[
        Union[
            FailedResult,
            FaceRegisterResult,
            FaceQualityResult,
            FaceAntiSpoofResult,
            FaceBestMatchResult,
            FaceMatchResult
        ]
    ]

    def __init__(
        self,
        status: TaskStatus,
        result: Union[
            FailedResult,
            FaceRegisterResult,
            FaceQualityResult,
            FaceAntiSpoofResult,
            FaceBestMatchResult,
            FaceMatchResult,
        ] = None,
    ) -> None:
        super().__init__(status=status, result=result)


class Task(BaseTask):
    result: Optional[FailedResult]

    def __init__(
            self, 
            status: TaskStatus, 
            result: FailedResult = None
    ) -> None:
        super().__init__(status=status, result=result)


class FaceRegisterTask(BaseTask):
    result: FaceRegisterResult

    def __init__(
            self, 
            status: TaskStatus, 
            result: FaceRegisterResult
    ) -> None:
        super().__init__(status=status, result=result)


class FaceQualityTask(BaseTask):
    result: FaceQualityResult

    def __init__(
            self, 
            status: TaskStatus, 
            result: FaceQualityResult
    ) -> None:
        super().__init__(status=status, result=result)


class FaceAntiSpoofTask(BaseTask):
    result: FaceAntiSpoofResult

    def __init__(
            self, 
            status: TaskStatus, 
            result: FaceAntiSpoofResult
    ) -> None:
        super().__init__(status=status, result=result)


class FaceBestMatchTask(BaseTask):
    result: FaceBestMatchResult

    def __init__(
            self, 
            status: TaskStatus, 
            result: FaceBestMatchResult
    ) -> None:
        super().__init__(status=status, result=result)


class FaceMatchTask(BaseTask):
    result: FaceMatchResult

    def __init__(
            self, 
            status: TaskStatus, 
            result: FaceMatchResult
    ) -> None:
        super().__init__(status=status, result=result)
