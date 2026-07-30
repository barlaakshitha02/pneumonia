
import numpy as np

from tensorflow.keras.models import load_model

from config import (
    MODEL_PATH,
    CLASS_NAMES
)

from services.image_preprocessor import preprocess_image


print("Loading model...")

model = load_model(MODEL_PATH)

print("Model loaded successfully")


def predict_image(image_path):

    image = preprocess_image(image_path)


    prediction = model.predict(
        image,
        verbose=0
    )


    predicted_class = np.argmax(prediction)


    confidence = float(
        np.max(prediction)
    )


    return (
        CLASS_NAMES[predicted_class],
        confidence
    )