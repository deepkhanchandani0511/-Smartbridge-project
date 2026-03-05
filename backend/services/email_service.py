"""
Email delivery service using Gmail SMTP
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os
from utils import get_logger
from config import GMAIL_EMAIL, GMAIL_PASSWORD

logger = get_logger(__name__)

class EmailService:
    """Email delivery service using Gmail SMTP"""

    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587

    @staticmethod
    def send_photo_email(recipient_email: str, photo_path: str, subject: str = None, body: str = None) -> dict:
        """
        Send photo via email using Gmail SMTP
        Requires GMAIL_EMAIL and GMAIL_PASSWORD environment variables
        """
        try:
            if not GMAIL_EMAIL or not GMAIL_PASSWORD:
                logger.error("Gmail credentials not configured in environment variables")
                return {
                    'success': False,
                    'error': 'Gmail credentials not configured'
                }

            if not os.path.exists(photo_path):
                logger.error(f"Photo file not found: {photo_path}")
                return {
                    'success': False,
                    'error': 'Photo file not found'
                }

            # Prepare email
            subject = subject or 'Photo from Drishyamitra'
            body = body or 'Here is a photo shared from Drishyamitra - AI Photo Management System'

            # Create message
            message = MIMEMultipart()
            message['From'] = GMAIL_EMAIL
            message['To'] = recipient_email
            message['Subject'] = subject

            # Add body
            message.attach(MIMEText(body, 'plain'))

            # Attach photo
            filename = os.path.basename(photo_path)
            with open(photo_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())

            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= {filename}')
            message.attach(part)

            # Send email
            logger.info(f"Connecting to Gmail SMTP server")
            server = smtplib.SMTP(EmailService.SMTP_SERVER, EmailService.SMTP_PORT)
            server.starttls()
            server.login(GMAIL_EMAIL, GMAIL_PASSWORD)

            logger.info(f"Sending email to {recipient_email}")
            server.send_message(message)
            server.quit()

            logger.info(f"Email sent successfully to {recipient_email}")
            return {
                'success': True,
                'recipient': recipient_email,
                'message': 'Email sent successfully'
            }

        except smtplib.SMTPAuthenticationError:
            logger.error("Gmail authentication failed - check credentials")
            return {
                'success': False,
                'error': 'Authentication failed - invalid Gmail credentials'
            }
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error: {str(e)}")
            return {
                'success': False,
                'error': f'SMTP error: {str(e)}'
            }
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    @staticmethod
    def send_bulk_photos(recipient_email: str, photo_paths: list, subject: str = None) -> dict:
        """Send multiple photos via email"""
        try:
            if not GMAIL_EMAIL or not GMAIL_PASSWORD:
                logger.error("Gmail credentials not configured")
                return {
                    'success': False,
                    'error': 'Gmail credentials not configured'
                }

            # Prepare email
            subject = subject or 'Photos from Drishyamitra'
            body = f'Here are {len(photo_paths)} photos shared from Drishyamitra'

            message = MIMEMultipart()
            message['From'] = GMAIL_EMAIL
            message['To'] = recipient_email
            message['Subject'] = subject

            message.attach(MIMEText(body, 'plain'))

            # Attach all photos
            for photo_path in photo_paths:
                if os.path.exists(photo_path):
                    filename = os.path.basename(photo_path)
                    with open(photo_path, 'rb') as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())

                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename= {filename}')
                    message.attach(part)

            # Send email
            server = smtplib.SMTP(EmailService.SMTP_SERVER, EmailService.SMTP_PORT)
            server.starttls()
            server.login(GMAIL_EMAIL, GMAIL_PASSWORD)
            server.send_message(message)
            server.quit()

            logger.info(f"Bulk email sent to {recipient_email} with {len(photo_paths)} photos")
            return {
                'success': True,
                'recipient': recipient_email,
                'count': len(photo_paths),
                'message': 'Bulk email sent successfully'
            }

        except Exception as e:
            logger.error(f"Error sending bulk email: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
