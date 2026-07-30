import os

# =====================================================
# Base Directory
# =====================================================

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# =====================================================
# Dataset Paths
# =====================================================

DATASET_PATH = os.path.join(BASE_DIR, "dataset", "chest_xray")

TRAIN_PATH = os.path.join(DATASET_PATH, "train")
VAL_PATH = os.path.join(DATASET_PATH, "val")
TEST_PATH = os.path.join(DATASET_PATH, "test")

# =====================================================
# Model Save Path
# =====================================================

MODEL_DIR = os.path.join(BASE_DIR, "flask_application", "model")

MODEL_PATH = os.path.join(MODEL_DIR, "pneumonia_model.keras")

# =====================================================
# Training Parameters
# =====================================================

IMAGE_SIZE = (128, 128)

BATCH_SIZE = 32

EPOCHS = 20

LEARNING_RATE = 0.0001

# =====================================================
# Class Labels
# =====================================================

CLASS_NAMES = {

    0: "NORMAL",

    1: "PNEUMONIA"

}