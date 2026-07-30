# from sklearn.metrics import classification_report, confusion_matrix
# import numpy as np
# from tensorflow.keras.models import load_model

# from data_loader import get_data_generators
# from config import MODEL_PATH, CLASS_NAMES


# # ===========================================
# # Load Test Data
# # ===========================================

# _, _, test_generator = get_data_generators()

# # ===========================================
# # Load Trained Model
# # ===========================================

# model = load_model(MODEL_PATH)

# print("✅ Model Loaded Successfully\n")

# # ===========================================
# # Evaluate Model
# # ===========================================

# loss, accuracy = model.evaluate(test_generator, verbose=1)

# print(f"\nTest Loss     : {loss:.4f}")
# print(f"Test Accuracy : {accuracy * 100:.2f}%")

# # ===========================================
# # Predictions
# # ===========================================

# predictions = model.predict(test_generator, verbose=1)

# predicted_classes = np.argmax(predictions, axis=1)

# true_classes = test_generator.classes

# class_labels = list(CLASS_NAMES.values())

# # ===========================================
# # Classification Report
# # ===========================================

# print("\nClassification Report\n")

# print(
#     classification_report(
#         true_classes,
#         predicted_classes,
#         target_names=class_labels
#     )
# )

# # ===========================================
# # Confusion Matrix
# # ===========================================

# print("\nConfusion Matrix\n")

# print(
#     confusion_matrix(
#         true_classes,
#         predicted_classes
#     )
# )


import os
import sys
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# ==========================================
# Add Project Root to Python Path
# ==========================================

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from config import (
    TEST_PATH,
    IMAGE_SIZE,
    BATCH_SIZE
)

# ==========================================
# Load Trained Model
# ==========================================

MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "flask_application",
    "model",
    "pneumonia_model.keras"
)

print("Loading trained model...")
model = load_model(MODEL_PATH)

print("Model Loaded Successfully!")

# ==========================================
# Test Data Generator
# ==========================================

test_datagen = ImageDataGenerator(rescale=1.0 / 255)

test_generator = test_datagen.flow_from_directory(
    TEST_PATH,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    shuffle=False
)

# ==========================================
# Evaluate Model
# ==========================================

print("\nEvaluating Model...\n")

loss, accuracy = model.evaluate(
    test_generator,
    verbose=1
)

print("\n==============================")
print(f"Test Loss     : {loss:.4f}")
print(f"Test Accuracy : {accuracy * 100:.2f}%")
print("==============================")

# ==========================================
# Predictions
# ==========================================

predictions = model.predict(
    test_generator,
    verbose=1
)

predicted_classes = np.argmax(predictions, axis=1)

true_classes = test_generator.classes

class_names = list(test_generator.class_indices.keys())

# ==========================================
# Classification Report
# ==========================================

print("\nClassification Report\n")

print(
    classification_report(
        true_classes,
        predicted_classes,
        target_names=class_names
    )
)

# ==========================================
# Confusion Matrix
# ==========================================

cm = confusion_matrix(
    true_classes,
    predicted_classes
)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=class_names
)

disp.plot(cmap="Blues")

plt.title("Confusion Matrix")

plt.show()