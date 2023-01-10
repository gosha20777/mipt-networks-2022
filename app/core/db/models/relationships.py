from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from core.db.models.base import Base


class UserRoles(Base):
    __tablename__ = 'user_roles'
    index = Column(
        'id', 
        Integer, 
        primary_key=True, 
        index=True, 
        autoincrement=True
    )
    user_id = Column(
        UUID(as_uuid=True), 
        ForeignKey('user.id'), primary_key=True
    )
    role_id = Column(
        String, 
        ForeignKey('role.id'), 
        primary_key=True
    )


class UserEngines(Base):
    __tablename__ = 'user_engines'
    index = Column(
        'id', 
        Integer, 
        primary_key=True, 
        index=True, 
        autoincrement=True
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('user.id'),
        primary_key=True
    )
    engine_id = Column(
        UUID(as_uuid=True), 
        ForeignKey('engine.id'), 
        primary_key=True
    )
