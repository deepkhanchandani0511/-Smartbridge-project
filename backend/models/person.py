"""
Person model for storing identified people
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config import Base

class Person(Base):
    """Person database model"""
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="people")
    faces = relationship("Face", back_populates="person", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Person(id={self.id}, name={self.name})>"
