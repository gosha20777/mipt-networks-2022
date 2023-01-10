from pydantic import BaseModel
from pydantic.fields import Field


class Pong(BaseModel):
    pong: str = Field(
        default='User Viewer, version X.Y.Z', 
        title='Pong', 
        description='pong response'
    )
