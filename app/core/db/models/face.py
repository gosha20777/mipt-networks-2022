import uuid

from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.db.models.base import Base


class Face(Base):
    face_id = Column('id', 
        UUID(as_uuid=True), 
        primary_key=True, 
        index=True, 
        default=uuid.uuid4
    )
    engine_id = Column(UUID(as_uuid=True), ForeignKey('engine.id'))
    is_active = Column(Boolean, nullable=False, default=True)
    # relations
    engine = relationship('Engine', back_populates='faces')
    descriptors = relationship('Descriptor')
