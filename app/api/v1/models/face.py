import uuid
from typing import List

from pydantic import BaseModel
from pydantic.fields import Field

from api.v1.models.common import MaxPageBase


class FaceResponse(BaseModel):
    engine_id: uuid.UUID = Field(
        default=uuid.uuid4(), 
        title='Engine Id', 
        description='Engine identificator (uuid)',
    )
    is_active: bool = Field(
        default=True, 
        title='Face Active Flag', 
        description='Face active flag'
    )
    descriptors: List[str] = Field(
        default=['a', 'b'], 
        title='Descriptors', 
        description='List with descriptors',
    )


class FacesResponse(MaxPageBase):
    faces: List[uuid.UUID] = Field(
        default=[uuid.uuid4(), uuid.uuid4()],
        title='Faces UUIDs',
        description='List with faces UUIDs',
    )
