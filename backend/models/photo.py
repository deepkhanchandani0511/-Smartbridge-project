"""
Photo model for storing photo metadata
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config import Base

class Photo(Base):
    """Photo database model"""
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    file_path = Column(String(255), nullable=False)
    filename = Column(String(255), nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    processed = Column(Integer, default=0)  # 0: pending, 1: processing, 2: completed, -1: failed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="photos")
    faces = relationship("Face", back_populates="photo", cascade="all, delete-orphan")
    deliveries = relationship("DeliveryHistory", back_populates="photo", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Photo(id={self.id}, filename={self.filename})>"
