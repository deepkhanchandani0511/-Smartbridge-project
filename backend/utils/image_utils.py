"""
Image processing utilities
"""
import cv2
import numpy as np
import os
from datetime import datetime
import uuid

class ImageUtils:
    """Image processing utilities"""

    @staticmethod
    def allowed_file(filename: str, allowed_extensions: set) -> bool:
        """Check if file has allowed extension"""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

    @staticmethod
    def save_uploaded_file(file, upload_folder: str) -> str:
        """Save uploaded file to folder"""
        os.makedirs(upload_folder, exist_ok=True)
        
        # Generate unique filename
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{timestamp}_{unique_id}.{file_extension}"
        
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        return filepath, filename

    @staticmethod
    def read_image(filepath: str) -> np.ndarray:
        """Read image from file"""
        if not os.path.exists(filepath):
            return None
        return cv2.imread(filepath)

    @staticmethod
    def get_image_dimensions(filepath: str) -> tuple:
        """Get image dimensions"""
        img = ImageUtils.read_image(filepath)
        if img is not None:
            return img.shape[:2]  # (height, width)
        return None

    @staticmethod
    def resize_image(image: np.ndarray, max_width: int = 1920, max_height: int = 1080) -> np.ndarray:
        """Resize image to fit within max dimensions"""
        height, width = image.shape[:2]
        
        if width <= max_width and height <= max_height:
            return image
        
        ratio = min(max_width / width, max_height / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        
        return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

    @staticmethod
    def draw_face_box(image: np.ndarray, x: int, y: int, w: int, h: int, label: str = None, color: tuple = (0, 255, 0)) -> np.ndarray:
        """Draw bounding box on image"""
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
        if label:
            cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        return image

    @staticmethod
    def crop_face(image: np.ndarray, x: int, y: int, w: int, h: int, padding: int = 10) -> np.ndarray:
        """Crop face from image with padding"""
        x_start = max(0, x - padding)
        y_start = max(0, y - padding)
        x_end = min(image.shape[1], x + w + padding)
        y_end = min(image.shape[0], y + h + padding)
        
        return image[y_start:y_end, x_start:x_end]

    @staticmethod
    def organize_photo_by_person(photo_path: str, organized_folder: str, person_name: str) -> str:
        """Organize photo into person-specific folder"""
        person_folder = os.path.join(organized_folder, person_name)
        os.makedirs(person_folder, exist_ok=True)
        
        filename = os.path.basename(photo_path)
        new_path = os.path.join(person_folder, filename)
        
        # Copy file to organized folder
        import shutil
        shutil.copy2(photo_path, new_path)
        
        return new_path
