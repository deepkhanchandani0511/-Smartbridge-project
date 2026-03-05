"""
Face model for storing detected face data and embeddings
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
import json
from config import Base

class Face(Base):
    """Face database model"""
    __tablename__ = 'faces'

    id = Column(Integer, primary_key=True, index=True)
    photo_id = Column(Integer, ForeignKey('photos.id'), nullable=False)
    person_id = Column(Integer, ForeignKey('people.id'), nullable=True)
    embedding_data = Column(String(5000), nullable=True)  # Store as JSON string
    bounding_box = Column(String(500), nullable=True)  # Format: "x,y,w,h"
    confidence = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    photo = relationship("Photo", back_populates="faces")
    person = relationship("Person", back_populates="faces")

    def set_embedding(self, embedding_list):
        """Store embedding as JSON string"""
        self.embedding_data = json.dumps(embedding_list)

    def get_embedding(self):
        """Retrieve embedding from JSON string"""
        if self.embedding_data:
            return json.loads(self.embedding_data)
        return None

    def __repr__(self):
        return f"<Face(id={self.id}, photo_id={self.photo_id}, person_id={self.person_id})>"
