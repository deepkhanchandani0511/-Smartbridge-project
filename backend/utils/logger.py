"""
Logging configuration for Drishyamitra
"""
import logging
import os
from datetime import datetime

class Logger:
    """Centralized logging configuration"""

    _logger = None

    @classmethod
    def get_logger(cls, name: str = 'drishyamitra') -> logging.Logger:
        """Get or create logger instance"""
        if cls._logger is None:
            cls._setup_logger(name)
        return cls._logger

    @classmethod
    def _setup_logger(cls, name: str):
        """Setup logger configuration"""
        cls._logger = logging.getLogger(name)
        cls._logger.setLevel(logging.DEBUG)

        # Create logs directory
        log_dir = 'logs'
        os.makedirs(log_dir, exist_ok=True)

        # File handler
        log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers
        cls._logger.addHandler(file_handler)
        cls._logger.addHandler(console_handler)

# Convenience functions
def get_logger(name: str = 'drishyamitra') -> logging.Logger:
    """Get logger instance"""
    return Logger.get_logger(name)

def log_info(message: str):
    """Log info level message"""
    Logger.get_logger().info(message)

def log_error(message: str, exc_info: bool = False):
    """Log error level message"""
    Logger.get_logger().error(message, exc_info=exc_info)

def log_debug(message: str):
    """Log debug level message"""
    Logger.get_logger().debug(message)

def log_warning(message: str):
    """Log warning level message"""
    Logger.get_logger().warning(message)
