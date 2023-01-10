from pydantic import BaseModel
from pydantic.fields import Field

from api.v1.models.common import ExpTtimeBase
from api.v1.models.enums import FileStatusType


class UploadFileResponse(ExpTtimeBase):
    file_hash: str = Field(
        default='8743b52063cd84097a65d1633f5c74f5', 
        title='File Id', 
        description='File identificator (md5)'
    )


class UploadFileStatusResponse(BaseModel):
    status: FileStatusType = Field(
        default=FileStatusType.available, 
        title='File Status', 
        description='File status in cache',
    )
