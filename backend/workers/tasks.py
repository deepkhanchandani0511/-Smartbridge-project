"""
Task definitions module
"""
from .celery_worker import (
    celery_app,
    process_photo_faces_task,
    organize_photos_task
)

__all__ = [
    'celery_app',
    'process_photo_faces_task',
    'organize_photos_task'
]
