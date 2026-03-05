"""
Routes package - API endpoint blueprints
"""
from .auth_routes import auth_bp
from .photo_routes import photo_bp
from .face_routes import face_bp
from .chat_routes import chat_bp
from .delivery_routes import delivery_bp

__all__ = [
    'auth_bp',
    'photo_bp',
    'face_bp',
    'chat_bp',
    'delivery_bp'
]
