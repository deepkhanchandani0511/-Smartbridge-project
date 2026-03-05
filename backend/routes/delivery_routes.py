"""
Delivery routes for email and WhatsApp delivery
"""
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from config import SessionLocal
from models import Photo
from utils import token_required, get_logger
from services import DeliveryService, EmailService, WhatsAppService

delivery_bp = Blueprint('delivery', __name__, url_prefix='/api/delivery')
logger = get_logger(__name__)

def get_db():
    """Get database session"""
    return SessionLocal()

@delivery_bp.route('/email', methods=['POST'])
@token_required
def send_email_delivery(user_id):
    """Send photo via email"""
    try:
        data = request.get_json()
        photo_id = data.get('photo_id')
        recipient_email = data.get('recipient')

        if not photo_id or not recipient_email:
            return jsonify({'error': 'photo_id and recipient required'}), 400

        # Validate email
        if not EmailService.validate_email(recipient_email):
            return jsonify({'error': 'Invalid email format'}), 400

        db = get_db()

        # Verify photo exists
        photo = db.query(Photo).filter(
            Photo.id == photo_id,
            Photo.user_id == user_id
        ).first()

        if not photo:
            db.close()
            return jsonify({'error': 'Photo not found'}), 404

        # Send delivery
        result = DeliveryService.deliver_photo(
            user_id=user_id,
            photo_id=photo_id,
            method='email',
            recipient=recipient_email,
            db=db
        )

        db.close()

        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        db.close()
        return jsonify({'error': 'Email delivery failed'}), 500

@delivery_bp.route('/whatsapp', methods=['POST'])
@token_required
def send_whatsapp_delivery(user_id):
    """Send photo via WhatsApp"""
    try:
        data = request.get_json()
        photo_id = data.get('photo_id')
        recipient_phone = data.get('recipient')

        if not photo_id or not recipient_phone:
            return jsonify({'error': 'photo_id and recipient required'}), 400

        # Validate phone
        if not WhatsAppService.validate_phone(recipient_phone):
            return jsonify({'error': 'Invalid phone number format'}), 400

        db = get_db()

        # Verify photo exists
        photo = db.query(Photo).filter(
            Photo.id == photo_id,
            Photo.user_id == user_id
        ).first()

        if not photo:
            db.close()
            return jsonify({'error': 'Photo not found'}), 404

        # Send delivery
        result = DeliveryService.deliver_photo(
            user_id=user_id,
            photo_id=photo_id,
            method='whatsapp',
            recipient=recipient_phone,
            db=db
        )

        db.close()

        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        logger.error(f"Error sending WhatsApp: {str(e)}")
        db.close()
        return jsonify({'error': 'WhatsApp delivery failed'}), 500

@delivery_bp.route('/history', methods=['GET'])
@token_required
def get_delivery_history(user_id):
    """Get delivery history for user"""
    try:
        db = get_db()

        history = DeliveryService.get_delivery_history(user_id, db)
        stats = DeliveryService.get_delivery_stats(user_id, db)

        db.close()

        return jsonify({
            'history': history,
            'stats': stats
        }), 200

    except Exception as e:
        logger.error(f"Error getting delivery history: {str(e)}")
        db.close()
        return jsonify({'error': 'Failed to get delivery history'}), 500

@delivery_bp.route('/stats', methods=['GET'])
@token_required
def get_delivery_stats_endpoint(user_id):
    """Get delivery statistics"""
    try:
        db = get_db()

        stats = DeliveryService.get_delivery_stats(user_id, db)

        db.close()

        return jsonify(stats), 200

    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        db.close()
        return jsonify({'error': 'Failed to get stats'}), 500
