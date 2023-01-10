from pydantic import BaseModel


class EngineVersion(BaseModel):
    major: int 
    minor: int 
    path: int
