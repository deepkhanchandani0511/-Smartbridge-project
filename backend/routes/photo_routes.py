"""
Photo routes for photo upload and management
"""
from flask import Blueprint, request, jsonify, send_file
from sqlalchemy.orm import Session
from config import SessionLocal, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from models import Photo, User
from utils import AuthUtils, ImageUtils, token_required, get_logger
from services import FaceService
import os
from werkzeug.utils import secure_filename

photo_bp = Blueprint('photo', __name__, url_prefix='/api/photos')
logger = get_logger(__name__)

def get_db():
    """Get database session"""
    return SessionLocal()

@photo_bp.route('/upload', methods=['POST'])
@token_required
def upload_photo(user_id):
    """Upload photo endpoint"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not ImageUtils.allowed_file(file.filename, ALLOWED_EXTENSIONS):
            return jsonify({'error': f'Only {", ".join(ALLOWED_EXTENSIONS)} files are allowed'}), 400

        # Save file
        filepath, filename = ImageUtils.save_uploaded_file(file, UPLOAD_FOLDER)

        db = get_db()

        # Create photo record
        photo = Photo(
            user_id=user_id,
            file_path=filepath,
            filename=filename,
            processed=0  # Mark as pending
        )
        db.add(photo)
        db.commit()
        db.refresh(photo)

        logger.info(f"Photo uploaded by user {user_id}: {filename}")

        # Trigger background task for face detection
        # This would normally be done with Celery
        from services import FaceService
        faces = FaceService.detect_faces(filepath)

        db.close()

        return jsonify({
            'message': 'Photo uploaded successfully',
            'photo': {
                'id': photo.id,
                'filename': filename,
                'faces_detected': len(faces)
            }
        }), 201

    except Exception as e:
        logger.error(f"Error uploading photo: {str(e)}")
        return jsonify({'error': 'Upload failed'}), 500

@photo_bp.route('/list', methods=['GET'])
@token_required
def list_photos(user_id):
    """List all photos for a user"""
    try:
        db = get_db()

        photos = db.query(Photo).filter(Photo.user_id == user_id).order_by(
            Photo.upload_date.desc()
        ).all()

        db.close()

        return jsonify({
            'photos': [{
                'id': p.id,
                'filename': p.filename,
                'upload_date': p.upload_date.isoformat(),
                'processed': p.processed
            } for p in photos]
        }), 200

    except Exception as e:
        logger.error(f"Error listing photos: {str(e)}")
        return jsonify({'error': 'Failed to list photos'}), 500

@photo_bp.route('/<int:photo_id>', methods=['GET'])
@token_required
def get_photo_details(user_id, photo_id):
    """Get photo details with faces"""
    try:
        db = get_db()

        photo = db.query(Photo).filter(
            Photo.id == photo_id,
            Photo.user_id == user_id
        ).first()

        if not photo:
            db.close()
            return jsonify({'error': 'Photo not found'}), 404

        from models import Face
        faces = db.query(Face).filter(Face.photo_id == photo_id).all()

        db.close()

        return jsonify({
            'photo': {
                'id': photo.id,
                'filename': photo.filename,
                'upload_date': photo.upload_date.isoformat(),
                'processed': photo.processed,
                'faces': [{
                    'id': f.id,
                    'person_id': f.person_id,
                    'bounding_box': f.bounding_box,
                    'confidence': f.confidence
                } for f in faces]
            }
        }), 200

    except Exception as e:
        logger.error(f"Error getting photo details: {str(e)}")
        return jsonify({'error': 'Failed to get photo details'}), 500

@photo_bp.route('/<int:photo_id>', methods=['DELETE'])
@token_required
def delete_photo(user_id, photo_id):
    """Delete a photo"""
    try:
        db = get_db()

        photo = db.query(Photo).filter(
            Photo.id == photo_id,
            Photo.user_id == user_id
        ).first()

        if not photo:
            db.close()
            return jsonify({'error': 'Photo not found'}), 404

        # Delete file
        if os.path.exists(photo.file_path):
            os.remove(photo.file_path)

        # Delete photo record (cascades to faces and deliveries)
        db.delete(photo)
        db.commit()
        db.close()

        logger.info(f"Photo deleted: {photo_id}")

        return jsonify({'message': 'Photo deleted successfully'}), 200

    except Exception as e:
        logger.error(f"Error deleting photo: {str(e)}")
        db.rollback()
        db.close()
        return jsonify({'error': 'Failed to delete photo'}), 500

@photo_bp.route('/<int:photo_id>/file', methods=['GET'])
@token_required
def get_photo_file(user_id, photo_id):
    """Download photo file"""
    try:
        db = get_db()

        photo = db.query(Photo).filter(
            Photo.id == photo_id,
            Photo.user_id == user_id
        ).first()

        db.close()

        if not photo or not os.path.exists(photo.file_path):
            return jsonify({'error': 'Photo not found'}), 404

        return send_file(photo.file_path, as_attachment=True, download_name=photo.filename)

    except Exception as e:
        logger.error(f"Error downloading photo: {str(e)}")
        return jsonify({'error': 'Failed to download photo'}), 500
