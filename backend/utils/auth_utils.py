"""
Authentication utilities for JWT and password handling
"""
from datetime import datetime, timedelta
import jwt
from bcrypt import hashpw, checkpw, gensalt
import os
from config import JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES

class AuthUtils:
    """Authentication utility functions"""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt"""
        if isinstance(password, str):
            password = password.encode('utf-8')
        return hashpw(password, gensalt()).decode('utf-8')

    @staticmethod
    def verify_password(password: str, hash_: str) -> bool:
        """Verify a password against its hash"""
        if isinstance(password, str):
            password = password.encode('utf-8')
        if isinstance(hash_, str):
            hash_ = hash_.encode('utf-8')
        return checkpw(password, hash_)

    @staticmethod
    def create_access_token(user_id: int, expires_delta: timedelta = None) -> str:
        """Create JWT access token"""
        if expires_delta is None:
            expires_delta = JWT_ACCESS_TOKEN_EXPIRES
        
        expire = datetime.utcnow() + expires_delta
        to_encode = {'user_id': user_id, 'exp': expire}
        
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm='HS256')
        return encoded_jwt

    @staticmethod
    def decode_access_token(token: str) -> dict:
        """Decode and verify JWT access token"""
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return {'error': 'Token has expired'}
        except jwt.InvalidTokenError:
            return {'error': 'Invalid token'}

    @staticmethod
    def get_user_from_token(token: str) -> int or None:
        """Extract user_id from token"""
        payload = AuthUtils.decode_access_token(token)
        if 'error' not in payload:
            return payload.get('user_id')
        return None

def token_required(f):
    """Decorator for protecting routes that require JWT"""
    from functools import wraps
    from flask import request, jsonify
    
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        payload = AuthUtils.decode_access_token(token)
        if 'error' in payload:
            return jsonify({'error': payload['error']}), 401
        
        kwargs['user_id'] = payload.get('user_id')
        return f(*args, **kwargs)
    
    return decorated
