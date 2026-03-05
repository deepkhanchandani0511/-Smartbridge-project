"""
WhatsApp delivery service
Supports both WhatsApp Web API and Twilio integration
"""
import requests
from utils import get_logger
from config import WHATSAPP_API_URL

logger = get_logger(__name__)

class WhatsAppService:
    """WhatsApp delivery service"""

    @staticmethod
    def send_photo_whatsapp(recipient_phone: str, photo_path: str, caption: str = None) -> dict:
        """
        Send photo via WhatsApp
        Works with whatsapp-web.js running on localhost:3001
        """
        try:
            caption = caption or 'Photo from Drishyamitra'

            # Prepare payload
            payload = {
                'to': recipient_phone,
                'image': photo_path,
                'caption': caption
            }

            # Send request to WhatsApp Web API
            response = requests.post(
                f'{WHATSAPP_API_URL}/api/send-image',
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                logger.info(f"WhatsApp photo sent to {recipient_phone}")
                return {
                    'success': True,
                    'recipient': recipient_phone,
                    'message': 'Photo sent via WhatsApp'
                }
            else:
                logger.error(f"WhatsApp API error: {response.text}")
                return {
                    'success': False,
                    'error': f'WhatsApp API error: {response.status_code}'
                }

        except requests.exceptions.ConnectionError:
            logger.error("Could not connect to WhatsApp Web API")
            return {
                'success': False,
                'error': 'WhatsApp Web API not available. Ensure it is running on localhost:3001'
            }
        except Exception as e:
            logger.error(f"Error sending WhatsApp photo: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    @staticmethod
    def send_message_whatsapp(recipient_phone: str, message: str) -> dict:
        """Send text message via WhatsApp"""
        try:
            payload = {
                'to': recipient_phone,
                'message': message
            }

            response = requests.post(
                f'{WHATSAPP_API_URL}/api/send-message',
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                logger.info(f"WhatsApp message sent to {recipient_phone}")
                return {
                    'success': True,
                    'recipient': recipient_phone,
                    'message': 'Message sent via WhatsApp'
                }
            else:
                logger.error(f"WhatsApp API error: {response.text}")
                return {
                    'success': False,
                    'error': f'WhatsApp API error: {response.status_code}'
                }

        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format"""
        import re
        # Accept formats: +1234567890, 1234567890, +1 234 567 8900
        pattern = r'^\+?1?\d{9,15}$'
        clean_phone = re.sub(r'[\s\-\(\)]', '', phone)
        return re.match(pattern, clean_phone) is not None

    @staticmethod
    def send_bulk_photos_whatsapp(recipient_phone: str, photo_paths: list, caption: str = None) -> dict:
        """Send multiple photos via WhatsApp"""
        try:
            caption = caption or f'Shared {len(photo_paths)} photos from Drishyamitra'

            payload = {
                'to': recipient_phone,
                'images': photo_paths,
                'caption': caption
            }

            response = requests.post(
                f'{WHATSAPP_API_URL}/api/send-images',
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                logger.info(f"Bulk WhatsApp photos sent to {recipient_phone}")
                return {
                    'success': True,
                    'recipient': recipient_phone,
                    'count': len(photo_paths),
                    'message': 'Photos sent via WhatsApp'
                }
            else:
                logger.error(f"WhatsApp API error: {response.text}")
                return {
                    'success': False,
                    'error': f'WhatsApp API error: {response.status_code}'
                }

        except Exception as e:
            logger.error(f"Error sending bulk WhatsApp photos: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
