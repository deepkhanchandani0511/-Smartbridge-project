"""
Main Flask application for Drishyamitra
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from config import config, init_db, Base, SessionLocal
from routes import auth_bp, photo_bp, face_bp, chat_bp, delivery_bp
from utils import get_logger
from datetime import datetime

logger = get_logger(__name__)

def create_app():
    """Create and configure Flask application"""
    
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config)
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize database
    try:
        init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(photo_bp)
    app.register_blueprint(face_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(delivery_bp)
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'ok',
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'Drishyamitra API'
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'error': 'Method not allowed'}), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {str(error)}")
        return jsonify({'error': 'Internal server error'}), 500
    
    # Request logging middleware
    @app.before_request
    def log_request():
        logger.debug(f"{request.method} {request.path}")
    
    @app.after_request
    def log_response(response):
        logger.debug(f"Response: {response.status_code}")
        return response
    
    logger.info("Flask application created and configured")
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
