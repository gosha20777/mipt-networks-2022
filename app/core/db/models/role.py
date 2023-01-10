from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from core.db.models.base import Base
from core.db.models.relationships import UserRoles


class Role(Base):
    role_id = Column(
        'id',
        String, 
        primary_key=True, 
        index=True
    )
    description = Column(String)
    # relations
    users = relationship(
        'User',
        secondary='user_roles',
        back_populates='roles'
    )
