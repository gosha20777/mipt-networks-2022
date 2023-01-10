import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.db.models.base import Base
from core.db.models.relationships import UserEngines, UserRoles


class User(Base):
    user_id = Column(
        'id',
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4
    )
    name = Column(
        'name',
        String(25),
        unique=True,
        nullable=False
    )
    password = Column(
        'password',
        String,
        nullable=False
    )
    date = Column(
        'date',
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    # relations
    roles = relationship(
        'Role',
        secondary='user_roles',
        back_populates='users'
    )
    engines = relationship(
        'Engine',
        secondary='user_engines',
        back_populates='users'
    )
