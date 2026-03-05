"""
Configuration module for Drishyamitra backend
Handles environment variables, database setup, and app configuration
"""
import os
from datetime import timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Environment variables
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///drishyamitra.db')
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
GMAIL_EMAIL = os.getenv('GMAIL_EMAIL', '')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD', '')
WHATSAPP_API_URL = os.getenv('WHATSAPP_API_URL', 'http://localhost:3001')

# Celery Configuration
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

# JWT Configuration
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

# Upload Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'data/uploads')
ORGANIZED_FOLDER = os.path.join(os.path.dirname(__file__), 'data/organized')
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# DeepFace Configuration
DEEPFACE_MODELS = ['Facenet512']  # Primary model
DEEPFACE_DISTANCE_METRIC = 'cosine'
DEEPFACE_SIMILARITY_THRESHOLD = 0.6

# Database Setup
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables on import
def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)

# Flask app configuration
class Config:
    """Base configuration"""
    TESTING = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = SECRET_KEY
    JWT_SECRET_KEY = JWT_SECRET_KEY

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Get configuration based on environment
ENV = os.getenv('ENV', 'development')
if ENV == 'production':
    config = ProductionConfig
elif ENV == 'testing':
    config = TestingConfig
else:
    config = DevelopmentConfig
