"""
Face detection and recognition service using DeepFace
"""
import numpy as np
import json
from sqlalchemy.orm import Session
from models import Face, Person, Photo
from utils import get_logger, ImageUtils
from config import DEEPFACE_MODELS, DEEPFACE_DISTANCE_METRIC, DEEPFACE_SIMILARITY_THRESHOLD

logger = get_logger(__name__)

# Try importing DeepFace, but provide fallback
try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except ImportError:
    logger.warning("DeepFace not available, using mock face detection")
    DEEPFACE_AVAILABLE = False

class FaceService:
    """Face detection and recognition service"""

    @staticmethod
    def detect_faces(image_path: str) -> list:
        """
        Detect faces in image using DeepFace
        Returns list of face data with bounding boxes
        """
        try:
            if not DEEPFACE_AVAILABLE:
                logger.warning(f"DeepFace not available, returning empty face list for {image_path}")
                return []
                
            logger.info(f"Detecting faces in {image_path}")
            
            # Read image
            img = ImageUtils.read_image(image_path)
            if img is None:
                logger.error(f"Could not read image: {image_path}")
                return []

            # Detect faces using DeepFace
            faces = DeepFace.extract_faces(
                img_path=image_path,
                model_name='Retina',  # RetinaFace for accurate detection
                detector_backend='opencv',
                expand_percentage=10,
                enforce_detection=False
            )

            logger.info(f"Found {len(faces)} faces in image")
            return faces

        except Exception as e:
            logger.error(f"Error detecting faces: {str(e)}")
            return []

    @staticmethod
    def get_face_embedding(image_path: str, face_data: dict = None) -> np.ndarray:
        """
        Generate embedding vector for a face using Facenet512
        """
        try:
            logger.debug(f"Generating embedding for face")
            
            # Generate embedding using Facenet512
            embedding = DeepFace.represent(
                img_path=image_path,
                model_name='Facenet512',
                enforce_detection=False
            )

            if embedding and len(embedding) > 0:
                return embedding[0]['embedding']
            return None

        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            return None

    @staticmethod
    def compare_embeddings(embedding1: list, embedding2: list, metric: str = DEEPFACE_DISTANCE_METRIC) -> float:
        """
        Compare two face embeddings using cosine similarity or euclidean distance
        Returns similarity score (higher = more similar)
        """
        try:
            if embedding1 is None or embedding2 is None:
                return 0.0

            embedding1 = np.array(embedding1)
            embedding2 = np.array(embedding2)

            if metric == 'cosine':
                # Cosine similarity (1 = identical, 0 = completely different)
                from scipy.spatial.distance import cosine
                distance = cosine(embedding1, embedding2)
                similarity = 1 - distance
            else:  # euclidean
                from scipy.spatial.distance import euclidean
                distance = euclidean(embedding1, embedding2)
                similarity = 1 / (1 + distance)

            return float(similarity)

        except Exception as e:
            logger.error(f"Error comparing embeddings: {str(e)}")
            return 0.0

    @staticmethod
    def find_matching_person(embedding: list, user_id: int, db: Session, threshold: float = DEEPFACE_SIMILARITY_THRESHOLD) -> Person:
        """
        Find matching person from database using embedding similarity
        """
        try:
            logger.debug(f"Searching for matching person")
            
            # Get all faces for this user
            user_faces = db.query(Face).join(Photo).filter(
                Photo.user_id == user_id,
                Face.person_id != None
            ).all()

            best_match = None
            best_similarity = 0.0

            for face in user_faces:
                if face.embedding_data:
                    stored_embedding = json.loads(face.embedding_data)
                    similarity = FaceService.compare_embeddings(embedding, stored_embedding)

                    if similarity > best_similarity:
                        best_similarity = similarity
                        best_match = face.person

            if best_similarity >= threshold and best_match:
                logger.info(f"Found matching person: {best_match.name} (similarity: {best_similarity:.2f})")
                return best_match
            
            logger.info(f"No matching person found (best similarity: {best_similarity:.2f})")
            return None

        except Exception as e:
            logger.error(f"Error finding matching person: {str(e)}")
            return None

    @staticmethod
    def create_person(name: str, user_id: int, db: Session) -> Person:
        """Create new person entry"""
        try:
            person = Person(name=name, user_id=user_id)
            db.add(person)
            db.commit()
            db.refresh(person)
            logger.info(f"Created new person: {name}")
            return person
        except Exception as e:
            logger.error(f"Error creating person: {str(e)}")
            db.rollback()
            return None

    @staticmethod
    def save_face_data(photo_id: int, person_id: int, embedding: list, bounding_box: str, confidence: float, db: Session) -> Face:
        """Save face data to database"""
        try:
            face = Face(
                photo_id=photo_id,
                person_id=person_id,
                bounding_box=bounding_box,
                confidence=confidence
            )
            face.set_embedding(embedding)
            db.add(face)
            db.commit()
            db.refresh(face)
            logger.info(f"Saved face data for photo {photo_id}")
            return face
        except Exception as e:
            logger.error(f"Error saving face data: {str(e)}")
            db.rollback()
            return None

    @staticmethod
    def get_person_photos(person_id: int, db: Session) -> list:
        """Get all photos of a specific person"""
        try:
            photos = db.query(Photo).join(Face).filter(
                Face.person_id == person_id
            ).all()
            return photos
        except Exception as e:
            logger.error(f"Error getting person photos: {str(e)}")
            return []
