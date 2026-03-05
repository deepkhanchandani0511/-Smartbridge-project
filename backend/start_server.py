"""
Server startup script for Drishyamitra backend
"""
import os
import sys
from app import create_app
from utils import get_logger

logger = get_logger(__name__)

def start_server():
    """Start the Flask development server"""
    try:
        # Create Flask app
        app = create_app()
        
        # Get configuration from environment
        host = os.getenv('FLASK_HOST', '0.0.0.0')
        port = int(os.getenv('FLASK_PORT', 5000))
        debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
        
        logger.info(f"Starting Drishyamitra server on {host}:{port}")
        logger.info(f"Debug mode: {debug}")
        
        # Run server
        app.run(
            host=host,
            port=port,
            debug=debug,
            use_reloader=True
        )
        
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    start_server()
