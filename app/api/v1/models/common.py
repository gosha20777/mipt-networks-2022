import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel, validator
from pydantic.fields import Field


class MaxPageBase(BaseModel):
    max_page: int = Field(
        default=0, 
        title='Max Page', 
        description='Max page',
        le=99999
    )


class EngineListBase(BaseModel):
    engines: List[uuid.UUID] = Field(
        default=[uuid.uuid4(), uuid.uuid4()],
        title='Engine UUIDs',
        description='List with Engine UUIDs',
    )


class UserListBase(BaseModel):
    users: List[uuid.UUID] = Field(
        default=[uuid.uuid4(), uuid.uuid4()],
        title='Users UUIDs',
        description='List with users UUIDs',
    )


class UserIdBase(BaseModel):
    user_id: uuid.UUID = Field(
        default=uuid.uuid4(), 
        title='User Id', 
        description='User identificator (uuid)'
    )


class EngineIdBase(BaseModel):
    engine_id: uuid.UUID = Field(
        default=uuid.uuid4(), 
        title='Engine Id', 
        description='Engine identificator (uuid)'
    )


class UserNameBase(BaseModel):
    user: str = Field(
        default='user', 
        title='User Name', 
        description='User name',
        max_length=20
    )


class ExpTtimeBase(BaseModel):
    exp: int = Field(
        default=1735689600,
        title='Expired Time',
        description='expired time in unix time format',
    )


class DateBase(BaseModel):
    date: datetime = Field(
        default=datetime(1997, 9, 16, 1, 1, 1), 
        title='Registration Date', 
        description='Registration date',
    )

    @validator("date", pre=True)
    def parse_birthdate(cls, value):
        if isinstance(value, str):
            return datetime.strptime(
                value,
                "%Y-%m-%d"
            )
        return value
