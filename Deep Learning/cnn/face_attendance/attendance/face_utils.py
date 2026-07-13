"""
Face detection and recognition utilities using OpenCV and TensorFlow.
"""
import os
import cv2
import numpy as np
from django.conf import settings

# Path to Haar Cascade classifier
CASCADE_PATH = os.path.join(settings.BASE_DIR, 'haarcascade_frontalface_default.xml')

# Face image dimensions for the CNN
FACE_SIZE = 100

# Minimum confidence threshold for recognition (45%)
CONFIDENCE_THRESHOLD = 0.45


def get_face_detector():
    """Return an OpenCV Haar Cascade face detector."""
    if not os.path.exists(CASCADE_PATH):
        raise FileNotFoundError(
            f"Haar Cascade file not found at {CASCADE_PATH}. "
            "Please ensure haarcascade_frontalface_default.xml is in the project root."
        )
    return cv2.CascadeClassifier(CASCADE_PATH)


def detect_faces(image_array):
    """
    Detect faces in an image using Haar Cascade.

    Args:
        image_array: numpy array of the image (BGR format from OpenCV)

    Returns:
        List of (x, y, w, h) tuples for each detected face
    """
    detector = get_face_detector()
    gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)

    faces = detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=4,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    return faces


def extract_face(image_array, face_coords):
    """
    Extract and preprocess a single face from an image.

    Args:
        image_array: numpy array of the image
        face_coords: (x, y, w, h) tuple

    Returns:
        Preprocessed face image as numpy array (FACE_SIZE x FACE_SIZE x 3)
    """
    x, y, w, h = face_coords

    # Add padding around the face (15% on each side)
    pad_w = int(w * 0.15)
    pad_h = int(h * 0.15)

    y1 = max(0, y - pad_h)
    y2 = min(image_array.shape[0], y + h + pad_h)
    x1 = max(0, x - pad_w)
    x2 = min(image_array.shape[1], x + w + pad_w)

    face = image_array[y1:y2, x1:x2]
    face = cv2.resize(face, (FACE_SIZE, FACE_SIZE))

    return face


def preprocess_face_for_prediction(face_image):
    """
    Preprocess a face image for CNN prediction.

    Args:
        face_image: numpy array of shape (FACE_SIZE, FACE_SIZE, 3)

    Returns:
        Preprocessed image ready for model.predict()
    """
    face = face_image.astype('float32') / 255.0
    face = np.expand_dims(face, axis=0)
    return face


def decode_image_from_base64(base64_string):
    """
    Decode a base64-encoded image string to a numpy array.

    Args:
        base64_string: base64-encoded image data

    Returns:
        numpy array of the decoded image (BGR format)
    """
    import base64

    # Remove the data URL prefix if present
    if ',' in base64_string:
        base64_string = base64_string.split(',')[1]

    img_bytes = base64.b64decode(base64_string)
    img_array = np.frombuffer(img_bytes, dtype=np.uint8)
    image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    return image


def save_face_image(face_image, save_dir, image_index):
    """
    Save a face image to disk.

    Args:
        face_image: numpy array of the face
        save_dir: directory to save the image
        image_index: index number for the filename

    Returns:
        Path to the saved image
    """
    os.makedirs(save_dir, exist_ok=True)
    filename = f"face_{image_index:04d}.jpg"
    filepath = os.path.join(save_dir, filename)
    cv2.imwrite(filepath, face_image)
    return filepath
