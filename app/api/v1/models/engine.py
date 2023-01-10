from typing import Any, Dict, Optional

from pydantic import BaseModel
from pydantic.fields import Field

from api.v1.models.common import (
    DateBase,
    EngineIdBase,
    EngineListBase,
    MaxPageBase,
    UserListBase,
)
from api.v1.models.enums import EngineType


class EngineVersion(BaseModel):
    major: int = Field(
        default=1, 
        title='Major Version', 
        description='Major version',
        le=99999
    )
    minor: int = Field(
        default=0, 
        title='Minor Version', 
        description='Minor version',
        le=99999
    )
    path: int = Field(
        default=0, 
        title='Path Version', 
        description='Path version',
        le=99999
    )


class EngineBase(BaseModel):
    engine_type: EngineType = Field(
        default=EngineType.tevian, 
        title='Engine Type', 
        description='Engine type'
    )
    description: str = Field(
        default='Room 228', 
        title='Description', 
        description='Description',
        max_length=50
    )
    version: EngineVersion = Field(
        title='Engine Version', 
        description='Engine version'
    )


class EngineCreateRequest(EngineBase):
    pass


class EngineUpdateRequest(EngineBase):
    pass 


class EnginesResponse(EngineListBase, MaxPageBase):
    pass


class EngineMetadata(BaseModel):
    quality_threshold: Optional[float] = Field(
        default=0.6, 
        title='Quality Threshold', 
        description='Quality threshold'
    )
    anti_spoofing_threshold: Optional[float] = Field(
        default=0.6,
        title='Anti Spoofing Threshold',
        description='Anti spoofing threshold',
    )
    build: Optional[str] = Field(
        default='build-0.1.74', 
        title='Build Version', 
        description='Build version of core library',
    )
    extra: Optional[Dict[str, Any]] = Field(
        default={}, 
        title='Extra Matadata', 
        description='Extra matadata'
    )


class EngineResponse(EngineBase, UserListBase, DateBase):
    meta_data: Optional[EngineMetadata] = Field(
        title='Engine Metadata', 
        description='Engine metadata'    
    )


class EngineCreateResponse(EngineIdBase):
    pass
