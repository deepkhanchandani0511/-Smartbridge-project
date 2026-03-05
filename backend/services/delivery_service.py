"""
Delivery service for managing photo deliveries via email and WhatsApp
"""
from sqlalchemy.orm import Session
from models import DeliveryHistory, Photo
from utils import get_logger
from .email_service import EmailService
from .whatsapp_service import WhatsAppService
from datetime import datetime

logger = get_logger(__name__)

class DeliveryService:
    """Manage photo deliveries and track delivery history"""

    @staticmethod
    def deliver_photo(user_id: int, photo_id: int, method: str, recipient: str, db: Session) -> dict:
        """
        Deliver photo via email or WhatsApp
        method: 'email' or 'whatsapp'
        """
        try:
            # Get photo
            photo = db.query(Photo).filter(Photo.id == photo_id, Photo.user_id == user_id).first()
            if not photo:
                logger.error(f"Photo not found: {photo_id}")
                return {
                    'success': False,
                    'error': 'Photo not found'
                }

            # Create delivery record
            delivery = DeliveryHistory(
                user_id=user_id,
                photo_id=photo_id,
                method=method,
                recipient=recipient,
                status='pending'
            )

            if method == 'email':
                result = EmailService.send_photo_email(recipient, photo.file_path)
            elif method == 'whatsapp':
                result = WhatsAppService.send_photo_whatsapp(recipient, photo.file_path)
            else:
                return {
                    'success': False,
                    'error': 'Invalid delivery method'
                }

            # Update delivery status
            if result['success']:
                delivery.status = 'sent'
                logger.info(f"Photo delivered successfully via {method} to {recipient}")
            else:
                delivery.status = 'failed'
                delivery.error_message = result.get('error', 'Unknown error')
                logger.error(f"Photo delivery failed: {result.get('error')}")

            db.add(delivery)
            db.commit()
            db.refresh(delivery)

            return {
                'success': result['success'],
                'delivery_id': delivery.id,
                'message': result.get('message', result.get('error'))
            }

        except Exception as e:
            logger.error(f"Error in deliver_photo: {str(e)}")
            db.rollback()
            return {
                'success': False,
                'error': str(e)
            }

    @staticmethod
    def get_delivery_history(user_id: int, db: Session, limit: int = 50) -> list:
        """Get delivery history for a user"""
        try:
            deliveries = db.query(DeliveryHistory).filter(
                DeliveryHistory.user_id == user_id
            ).order_by(DeliveryHistory.timestamp.desc()).limit(limit).all()

            return [{
                'id': d.id,
                'photo_id': d.photo_id,
                'method': d.method,
                'recipient': d.recipient,
                'timestamp': d.timestamp.isoformat(),
                'status': d.status
            } for d in deliveries]

        except Exception as e:
            logger.error(f"Error getting delivery history: {str(e)}")
            return []

    @staticmethod
    def get_delivery_stats(user_id: int, db: Session) -> dict:
        """Get delivery statistics for a user"""
        try:
            total = db.query(DeliveryHistory).filter(
                DeliveryHistory.user_id == user_id
            ).count()

            sent = db.query(DeliveryHistory).filter(
                DeliveryHistory.user_id == user_id,
                DeliveryHistory.status == 'sent'
            ).count()

            failed = db.query(DeliveryHistory).filter(
                DeliveryHistory.user_id == user_id,
                DeliveryHistory.status == 'failed'
            ).count()

            email_count = db.query(DeliveryHistory).filter(
                DeliveryHistory.user_id == user_id,
                DeliveryHistory.method == 'email'
            ).count()

            whatsapp_count = db.query(DeliveryHistory).filter(
                DeliveryHistory.user_id == user_id,
                DeliveryHistory.method == 'whatsapp'
            ).count()

            return {
                'total': total,
                'sent': sent,
                'failed': failed,
                'email': email_count,
                'whatsapp': whatsapp_count
            }

        except Exception as e:
            logger.error(f"Error getting delivery stats: {str(e)}")
            return {}
