"""
Celery worker configuration and task definitions
"""
from celery import Celery
from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from utils import get_logger
from config import SessionLocal
from models import Photo
from services import FaceService

logger = get_logger(__name__)

# Initialize Celery
celery_app = Celery(
    'drishyamitra',
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@celery_app.task(name='drishyamitra.tasks.process_photo_faces')
def process_photo_faces_task(photo_id: int):
    """
    Background task to process faces in a photo
    """
    try:
        logger.info(f"Starting face processing for photo {photo_id}")
        
        db = SessionLocal()
        
        # Get photo
        photo = db.query(Photo).filter(Photo.id == photo_id).first()
        
        if not photo:
            logger.error(f"Photo {photo_id} not found")
            db.close()
            return {'success': False, 'error': 'Photo not found'}
        
        # Update status to processing
        photo.processed = 1
        db.commit()
        
        # Detect faces
        detected_faces = FaceService.detect_faces(photo.file_path)
        logger.info(f"Detected {len(detected_faces)} faces in photo {photo_id}")
        
        processed_count = 0
        
        for idx, face_data in enumerate(detected_faces):
            try:
                # Get embedding
                embedding = FaceService.get_face_embedding(photo.file_path, face_data)
                
                # Try to find matching person
                matching_person = FaceService.find_matching_person(embedding, photo.user_id, db)
                
                # Save face data
                FaceService.save_face_data(
                    photo_id=photo_id,
                    person_id=matching_person.id if matching_person else None,
                    embedding=embedding if embedding else [],
                    bounding_box=str(face_data.get('facial_area', {})),
                    confidence=face_data.get('confidence', 0),
                    db=db
                )
                
                processed_count += 1
                
            except Exception as e:
                logger.error(f"Error processing face {idx} in photo {photo_id}: {str(e)}")
        
        # Update photo processing status
        photo.processed = 2  # Completed
        db.commit()
        
        logger.info(f"Completed face processing for photo {photo_id}. Processed {processed_count} faces")
        
        db.close()
        
        return {
            'success': True,
            'photo_id': photo_id,
            'faces_processed': processed_count
        }
        
    except Exception as e:
        logger.error(f"Error in process_photo_faces_task: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

@celery_app.task(name='drishyamitra.tasks.organize_photos')
def organize_photos_task(user_id: int):
    """
    Background task to organize photos by person
    """
    try:
        logger.info(f"Starting photo organization for user {user_id}")
        
        db = SessionLocal()
        
        from models import Face
        from utils import ImageUtils
        from config import ORGANIZED_FOLDER
        
        # Get all photos with recognized faces
        faces = db.query(Face).join(Photo).filter(
            Photo.user_id == user_id,
            Face.person_id != None
        ).all()
        
        organized_count = 0
        
        for face in faces:
            try:
                if face.person and face.photo:
                    new_path = ImageUtils.organize_photo_by_person(
                        face.photo.file_path,
                        ORGANIZED_FOLDER,
                        face.person.name
                    )
                    organized_count += 1
                    logger.debug(f"Organized photo to {new_path}")
            except Exception as e:
                logger.error(f"Error organizing photo: {str(e)}")
        
        db.close()
        
        logger.info(f"Completed photo organization for user {user_id}. Organized {organized_count} photos")
        
        return {
            'success': True,
            'user_id': user_id,
            'photos_organized': organized_count
        }
        
    except Exception as e:
        logger.error(f"Error in organize_photos_task: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

if __name__ == '__main__':
    celery_app.start()
