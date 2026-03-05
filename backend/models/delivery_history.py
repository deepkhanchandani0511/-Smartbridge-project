"""
DeliveryHistory model for tracking photo deliveries
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config import Base

class DeliveryHistory(Base):
    """DeliveryHistory database model"""
    __tablename__ = 'delivery_history'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    photo_id = Column(Integer, ForeignKey('photos.id'), nullable=False)
    method = Column(String(50), nullable=False)  # 'email' or 'whatsapp'
    recipient = Column(String(255), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default='pending')  # 'pending', 'sent', 'failed'
    error_message = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="deliveries")
    photo = relationship("Photo", back_populates="deliveries")

    def __repr__(self):
        return f"<DeliveryHistory(id={self.id}, method={self.method}, status={self.status})>"
