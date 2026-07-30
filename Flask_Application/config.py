import os

# Base directory of the Flask Application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Secret key for Flask sessions
SECRET_KEY = "pneumonia_detection_secret_key"

# Upload folder
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

# Allowed image extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# Trained model path
MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "pneumonia_model.keras"
)

# Image size expected by the model
IMAGE_SIZE = (128, 128)

# Class labels
CLASS_NAMES = {
    0: "NORMAL",
    1: "PNEUMONIA"
}


# Maximum upload size (16 MB)
MAX_CONTENT_LENGTH = 16 * 1024 * 1024