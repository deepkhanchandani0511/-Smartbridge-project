"""
Chat service for natural language processing using Groq API
"""
from sqlalchemy.orm import Session
from models import Photo, Person, DeliveryHistory
from utils import get_logger
from config import GROQ_API_KEY
import re
from datetime import datetime, timedelta

logger = get_logger(__name__)

# Try importing Groq, but provide fallback
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    logger.warning("Groq not available, chat service disabled")
    GROQ_AVAILABLE = False
    Groq = None

class ChatService:
    """AI Chat assistant service using Groq API"""

    def __init__(self):
        """Initialize Groq client"""
        if not GROQ_AVAILABLE:
            logger.warning("Groq not available, chat service will be limited")
            return
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = "mixtral-8x7b-32768"  # or "llama-3.3-70b-versatile"

    def process_message(self, user_message: str, user_id: int, db: Session) -> dict:
        """
        Process user message and execute appropriate action
        Returns response with action and data
        """
        try:
            logger.info(f"Processing chat message from user {user_id}: {user_message}")

            # Clean and normalize message
            message = user_message.strip().lower()

            # Intent detection and action execution
            response = self._detect_intent_and_execute(message, user_id, db)

            return response

        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return {
                'response': 'Sorry, I encountered an error. Please try again.',
                'action': 'error',
                'data': None
            }

    def _detect_intent_and_execute(self, message: str, user_id: int, db: Session) -> dict:
        """Detect intent from message and execute action"""
        
        # Intent patterns
        if any(word in message for word in ['show', 'photos of', 'images of', 'pictures of']):
            return self._handle_show_photos(message, user_id, db)
        
        elif any(word in message for word in ['send', 'whatsapp', 'email', 'share']):
            return self._handle_send_photo(message, user_id, db)
        
        elif any(word in message for word in ['upload', 'recent', 'today', 'yesterday', 'recently']):
            return self._handle_recent_uploads(message, user_id, db)
        
        else:
            return self._get_ai_response(message, user_id, db)

    def _handle_show_photos(self, message: str, user_id: int, db: Session) -> dict:
        """Handle 'show photos of [person]' queries"""
        try:
            # Extract person name from message
            person_name = self._extract_person_name(message)
            
            if not person_name:
                return {
                    'response': 'I need a person name. Try: "Show photos of John"',
                    'action': 'show_photos',
                    'data': None
                }

            # Search for person
            person = db.query(Person).filter(
                Person.user_id == user_id,
                Person.name.ilike(f"%{person_name}%")
            ).first()

            if not person:
                return {
                    'response': f'No person named "{person_name}" found in your collection.',
                    'action': 'show_photos',
                    'data': None
                }

            # Get photos of this person
            from models import Face
            photos = db.query(Photo).join(Face).filter(
                Face.person_id == person.id
            ).all()

            photo_data = [{
                'id': p.id,
                'filename': p.filename,
                'upload_date': p.upload_date.isoformat()
            } for p in photos]

            response = f'Found {len(photos)} photos of {person.name}.'
            
            return {
                'response': response,
                'action': 'show_photos',
                'data': photo_data
            }

        except Exception as e:
            logger.error(f"Error in show photos: {str(e)}")
            return {
                'response': 'Error retrieving photos.',
                'action': 'show_photos',
                'data': None
            }

    def _handle_send_photo(self, message: str, user_id: int, db: Session) -> dict:
        """Handle 'send/share photo' queries"""
        try:
            method = 'whatsapp' if 'whatsapp' in message else 'email'
            recipient = self._extract_recipient(message)

            if not recipient:
                return {
                    'response': f'Please provide a {method} recipient. Example: "Send to john@gmail.com"',
                    'action': 'send_photo',
                    'data': None
                }

            return {
                'response': f'Ready to send to {recipient} via {method}. Please confirm.',
                'action': 'send_photo',
                'data': {
                    'method': method,
                    'recipient': recipient
                }
            }

        except Exception as e:
            logger.error(f"Error in send photo: {str(e)}")
            return {
                'response': 'Error processing send request.',
                'action': 'send_photo',
                'data': None
            }

    def _handle_recent_uploads(self, message: str, user_id: int, db: Session) -> dict:
        """Handle 'show recent/today/yesterday uploads' queries"""
        try:
            now = datetime.utcnow()
            
            if 'yesterday' in message:
                start_date = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0)
                end_date = (now - timedelta(days=1)).replace(hour=23, minute=59, second=59)
            elif 'today' in message or 'recent' in message:
                start_date = now.replace(hour=0, minute=0, second=0)
                end_date = now
            else:
                start_date = now - timedelta(days=7)
                end_date = now

            photos = db.query(Photo).filter(
                Photo.user_id == user_id,
                Photo.upload_date >= start_date,
                Photo.upload_date <= end_date
            ).order_by(Photo.upload_date.desc()).all()

            photo_data = [{
                'id': p.id,
                'filename': p.filename,
                'upload_date': p.upload_date.isoformat()
            } for p in photos]

            response = f'Found {len(photos)} uploads.'
            return {
                'response': response,
                'action': 'show_uploads',
                'data': photo_data
            }

        except Exception as e:
            logger.error(f"Error in recent uploads: {str(e)}")
            return {
                'response': 'Error retrieving uploads.',
                'action': 'show_uploads',
                'data': None
            }

    def _get_ai_response(self, message: str, user_id: int, db: Session) -> dict:
        """Get response from Groq AI"""
        try:
            # Create context about user's photos
            total_photos = db.query(Photo).filter(Photo.user_id == user_id).count()
            total_people = db.query(Person).filter(Person.user_id == user_id).count()

            system_prompt = f"""You are Drishyamitra, an AI photo management assistant.
The user has {total_photos} photos and {total_people} identified people in their collection.
Be helpful, friendly, and concise in your responses.
Focus on photo management, organization, and delivery capabilities."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
                max_tokens=500
            )

            ai_response = response.choices[0].message.content

            return {
                'response': ai_response,
                'action': 'chat',
                'data': None
            }

        except Exception as e:
            logger.error(f"Error getting AI response: {str(e)}")
            return {
                'response': 'I am having trouble understanding. Can you rephrase?',
                'action': 'chat',
                'data': None
            }

    @staticmethod
    def _extract_person_name(message: str) -> str:
        """Extract person name from message"""
        keywords = ['of', 'for', 'with']
        for keyword in keywords:
            if keyword in message:
                parts = message.split(keyword)
                if len(parts) > 1:
                    name = parts[-1].strip()
                    # Remove common words
                    name = re.sub(r'^(some|all|the|my|your)\s+', '', name).strip()
                    return name
        return None

    @staticmethod
    def _extract_recipient(message: str) -> str:
        """Extract recipient email or phone from message"""
        # Email regex
        email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
        email_match = re.search(email_pattern, message)
        if email_match:
            return email_match.group()
        
        # Phone pattern (simple)
        phone_pattern = r'\+?[0-9\s\-]{10,}'
        phone_match = re.search(phone_pattern, message)
        if phone_match:
            return phone_match.group()
        
        # Extract name after 'to'
        if ' to ' in message:
            parts = message.split(' to ')
            return parts[-1].strip()
        
        return None
