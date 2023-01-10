import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.db.models.base import Base
from core.db.models.relationships import UserEngines


class Engine(Base):
    engine_id = Column(
        'id', 
        UUID(as_uuid=True), 
        primary_key=True, 
        index=True, 
        default=uuid.uuid4
    )
    provider = Column('provider', String, nullable=False)
    date = Column(
        'date',
        DateTime, 
        nullable=False, 
        default=datetime.utcnow
    )
    description = Column(String)
    # relations
    users = relationship(
        'User', 
        secondary='user_engines', 
        back_populates='engines'
    )
    faces = relationship('Face')
