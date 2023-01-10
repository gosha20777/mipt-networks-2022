import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.db.models.base import Base


class Descriptor(Base):
    descriptor_id = Column(
        'id', 
        String, 
        primary_key=True, 
        index=True
    )
    face_id = Column(UUID(as_uuid=True), ForeignKey('face.id'))
    # relations
    face = relationship('Face', back_populates='descriptors')
