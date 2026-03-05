"""
Chat routes for AI chatbot
"""
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from config import SessionLocal
from utils import token_required, get_logger
from services import ChatService

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')
logger = get_logger(__name__)

def get_db():
    """Get database session"""
    return SessionLocal()

@chat_bp.route('', methods=['POST'])
@token_required
def chat_message(user_id):
    """Chat with AI assistant"""
    try:
        data = request.get_json()
        message = data.get('message')

        if not message:
            return jsonify({'error': 'Message is required'}), 400

        db = get_db()

        # Process message
        chat_service = ChatService()
        
        # Check if service is available
        if not hasattr(chat_service, 'client') or chat_service.client is None:
            response = {
                'action': 'message',
                'response': 'Chat service is temporarily unavailable. Please try again later.',
                'data': None
            }
        else:
            response = chat_service.process_message(message, user_id, db)

        db.close()

        logger.info(f"Chat message processed for user {user_id}")

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        db.close()
        return jsonify({'error': 'Chat processing failed'}), 500

@chat_bp.route('/suggestions', methods=['GET'])
@token_required
def get_chat_suggestions(user_id):
    """Get chat suggestions for the user"""
    try:
        suggestions = [
            "Show photos of [person name]",
            "Send photos to [email/phone]",
            "Show photos from today",
            "Show photos from yesterday",
            "List all people in my collection",
            "How many photos do I have?"
        ]

        return jsonify({
            'suggestions': suggestions
        }), 200

    except Exception as e:
        logger.error(f"Error getting suggestions: {str(e)}")
        return jsonify({'error': 'Failed to get suggestions'}), 500
