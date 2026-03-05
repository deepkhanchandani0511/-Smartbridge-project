"""
Face recognition routes
"""
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from config import SessionLocal
from models import Photo, Face, Person
from utils import token_required, get_logger
from services import FaceService

face_bp = Blueprint('face', __name__, url_prefix='/api/faces')
logger = get_logger(__name__)

def get_db():
    """Get database session"""
    return SessionLocal()

@face_bp.route('/process/<int:photo_id>', methods=['POST'])
@token_required
def process_photo_faces(user_id, photo_id):
    """Detect and process faces in a photo"""
    try:
        db = get_db()

        # Get photo
        photo = db.query(Photo).filter(
            Photo.id == photo_id,
            Photo.user_id == user_id
        ).first()

        if not photo:
            db.close()
            return jsonify({'error': 'Photo not found'}), 404

        # Detect faces
        detected_faces = FaceService.detect_faces(photo.file_path)

        processed_faces = []

        for idx, face_data in enumerate(detected_faces):
            try:
                # Get embedding
                embedding = FaceService.get_face_embedding(photo.file_path, face_data)

                # Try to find matching person
                matching_person = FaceService.find_matching_person(embedding, user_id, db)

                # Save face data
                face = FaceService.save_face_data(
                    photo_id=photo_id,
                    person_id=matching_person.id if matching_person else None,
                    embedding=embedding if embedding else [],
                    bounding_box=str(face_data.get('facial_area', {})),
                    confidence=face_data.get('confidence', 0),
                    db=db
                )

                processed_faces.append({
                    'id': face.id,
                    'person_id': face.person_id,
                    'person_name': matching_person.name if matching_person else 'Unknown',
                    'confidence': face.confidence
                })

            except Exception as e:
                logger.error(f"Error processing face {idx}: {str(e)}")

        # Update photo processing status
        photo.processed = 2  # Completed
        db.commit()
        db.close()

        logger.info(f"Processed {len(processed_faces)} faces in photo {photo_id}")

        return jsonify({
            'photo_id': photo_id,
            'faces_count': len(processed_faces),
            'faces': processed_faces
        }), 200

    except Exception as e:
        logger.error(f"Error processing faces: {str(e)}")
        db.rollback()
        db.close()
        return jsonify({'error': 'Face processing failed'}), 500

@face_bp.route('/<int:face_id>/label', methods=['PUT'])
@token_required
def label_face(user_id, face_id):
    """Label a face with a person name"""
    try:
        data = request.get_json()
        person_name = data.get('person_name')

        if not person_name:
            return jsonify({'error': 'Person name required'}), 400

        db = get_db()

        # Get face
        face = db.query(Face).join(Photo).filter(
            Face.id == face_id,
            Photo.user_id == user_id
        ).first()

        if not face:
            db.close()
            return jsonify({'error': 'Face not found'}), 404

        # Check if person exists
        person = db.query(Person).filter(
            Person.name.ilike(person_name),
            Person.user_id == user_id
        ).first()

        # Create new person if doesn't exist
        if not person:
            person = FaceService.create_person(person_name, user_id, db)

        # Update face
        face.person_id = person.id
        db.commit()
        db.close()

        logger.info(f"Face {face_id} labeled as {person_name}")

        return jsonify({
            'message': 'Face labeled successfully',
            'face': {
                'id': face.id,
                'person_id': person.id,
                'person_name': person.name
            }
        }), 200

    except Exception as e:
        logger.error(f"Error labeling face: {str(e)}")
        db.rollback()
        db.close()
        return jsonify({'error': 'Failed to label face'}), 500

@face_bp.route('/person/<int:person_id>', methods=['GET'])
@token_required
def get_person_faces(user_id, person_id):
    """Get all faces of a specific person"""
    try:
        db = get_db()

        # Verify person belongs to user
        person = db.query(Person).filter(
            Person.id == person_id,
            Person.user_id == user_id
        ).first()

        if not person:
            db.close()
            return jsonify({'error': 'Person not found'}), 404

        # Get all faces
        faces = db.query(Face).filter(Face.person_id == person_id).all()

        db.close()

        return jsonify({
            'person': {
                'id': person.id,
                'name': person.name,
                'faces_count': len(faces)
            },
            'faces': [{
                'id': f.id,
                'photo_id': f.photo_id,
                'confidence': f.confidence
            } for f in faces]
        }), 200

    except Exception as e:
        logger.error(f"Error getting person faces: {str(e)}")
        db.close()
        return jsonify({'error': 'Failed to get person faces'}), 500

@face_bp.route('/people', methods=['GET'])
@token_required
def get_all_people(user_id):
    """Get all identified people for the user"""
    try:
        db = get_db()

        people = db.query(Person).filter(Person.user_id == user_id).all()

        # Count faces for each person
        people_data = []
        for person in people:
            face_count = db.query(Face).filter(Face.person_id == person.id).count()
            people_data.append({
                'id': person.id,
                'name': person.name,
                'faces_count': face_count
            })

        db.close()

        return jsonify({
            'people_count': len(people_data),
            'people': people_data
        }), 200

    except Exception as e:
        logger.error(f"Error getting people: {str(e)}")
        db.close()
        return jsonify({'error': 'Failed to get people'}), 500
