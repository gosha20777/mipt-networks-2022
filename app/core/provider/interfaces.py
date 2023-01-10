import logging
from typing import Any, Dict, Optional, Union

from pydantic import BaseModel

from core.provider.models.engine import EngineVersion
from core.provider.models.enums import EngineType, OrchestratorType
from core.provider.models.tasks import (
    FaceAntiSpoofTask,
    FaceBestMatchTask,
    FaceMatchTask,
    FaceQualityTask,
    FaceRegisterTask,
    Task,
)


class OrchestratorConfig(BaseModel):
    orchestrator_type: OrchestratorType
    params: Optional[Dict[str, Any]]


class IProviderConfig(BaseModel):
    engine_type: EngineType
    version: EngineVersion
    description: str
    quality_threshold: float
    anti_spoofing_threshold: float
    build: str
    orchestrator: OrchestratorConfig


class IProvider:
    def __init__(self, config: IProviderConfig) -> None:
        self.__name = f'{config.engine_type}-{config.version.major}-{config.version.minor}-{config.version.path}'
        self.__description = config.description
        self.__quality_threshold = config.quality_threshold
        self.__anti_spoofing_threshold = config.anti_spoofing_threshold
        self.__build = config.build
        self.__orchestrator_type = config.orchestrator.orchestrator_type
        self.__params = config.orchestrator.params
        self.__logger = logging.getLogger(self.__name)

    def register(self, data: bytes) -> Union[FaceRegisterTask, Task]:
        """
        Register face in the engine db.
        """
        raise NotImplementedError()

    def quality(self, data: bytes) -> Union[FaceQualityTask, Task]:
        """
        Get quality of input image or video.
        """
        raise NotImplementedError()

    def liveness(self, data: bytes) -> Union[FaceAntiSpoofTask, Task]:
        """
        Get anti-spoofing score.
        """
        raise NotImplementedError()

    def best_match(self, data: bytes) -> Union[FaceBestMatchTask, Task]:
        """
        Get best match id.
        """
        raise NotImplementedError()

    def match_with_face(
            self, 
            data: bytes, 
            internal_id: str
    ) -> Union[FaceMatchTask, Task]:
        """
        Get match score.
        """
        raise NotImplementedError()

    def remove_face(self, internal_id: str) -> Task:
        """
        Remove face from engine's db.
        """

    @property
    def name(self) -> str:
        return self.__name

    @property
    def description(self) -> str:
        return self.__description

    @property
    def build(self) -> str:
        return self.__build

    @property
    def orchestrator_type(self) -> str:
        return self.__orchestrator_type

    @property
    def params(self) -> Optional[Dict[str, Any]]:
        return self.__params

    @property
    def _log(self) -> logging.Logger:
        return self.__logger
