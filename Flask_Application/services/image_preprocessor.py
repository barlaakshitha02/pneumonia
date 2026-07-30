import cv2
import numpy as np

from config import IMAGE_SIZE


def preprocess_image(image_path):
    """
    Read and preprocess the uploaded image.
    """

    # Read image
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Unable to read image.")

    # Resize image
    image = cv2.resize(image, IMAGE_SIZE)

    # Normalize pixel values
    image = image.astype("float32") / 255.0

    # Add batch dimension
    image = np.expand_dims(image, axis=0)

    return image