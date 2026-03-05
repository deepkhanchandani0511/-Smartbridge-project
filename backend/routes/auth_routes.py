"""
Authentication routes for user signup and login
"""
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from config import SessionLocal
from models import User
from utils import AuthUtils, get_logger
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
logger = get_logger(__name__)

def get_db():
    """Get database session"""
    return SessionLocal()

@auth_bp.route('/signup', methods=['POST'])
def signup():
    """User signup endpoint"""
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password required'}), 400

        email = data.get('email').strip().lower()
        password = data.get('password')

        # Validate email format
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return jsonify({'error': 'Invalid email format'}), 400

        # Validate password strength
        if len(password) < 8:
            return jsonify({'error': 'Password must be at least 8 characters long'}), 400

        db = get_db()
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            db.close()
            return jsonify({'error': 'Email already registered'}), 409

        # Hash password
        password_hash = AuthUtils.hash_password(password)

        # Create new user
        user = User(email=email, password_hash=password_hash)
        db.add(user)
        db.commit()
        db.refresh(user)
        db.close()

        logger.info(f"New user registered: {email}")

        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'email': user.email
            }
        }), 201

    except Exception as e:
        logger.error(f"Error in signup: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password required'}), 400

        email = data.get('email').strip().lower()
        password = data.get('password')

        db = get_db()

        # Find user
        user = db.query(User).filter(User.email == email).first()
        db.close()

        if not user:
            logger.warning(f"Login failed for non-existent user: {email}")
            return jsonify({'error': 'Invalid email or password'}), 401

        # Verify password
        if not AuthUtils.verify_password(password, user.password_hash):
            logger.warning(f"Login failed for user: {email} (wrong password)")
            return jsonify({'error': 'Invalid email or password'}), 401

        # Generate access token
        access_token = AuthUtils.create_access_token(user.id)

        logger.info(f"User logged in: {email}")

        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email
            }
        }), 200

    except Exception as e:
        logger.error(f"Error in login: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/verify', methods=['POST'])
def verify_token():
    """Verify JWT token validity"""
    try:
        token = request.headers.get('Authorization', '').split(' ')[-1]
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        payload = AuthUtils.decode_access_token(token)
        
        if 'error' in payload:
            return jsonify({'error': payload['error']}), 401

        return jsonify({
            'valid': True,
            'user_id': payload.get('user_id')
        }), 200

    except Exception as e:
        logger.error(f"Error verifying token: {str(e)}")
        return jsonify({'error': 'Invalid token'}), 401
