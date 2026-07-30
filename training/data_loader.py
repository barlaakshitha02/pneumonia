import os

from tensorflow.keras.preprocessing.image import ImageDataGenerator

from config import (
    TRAIN_PATH,
    VAL_PATH,
    TEST_PATH,
    IMAGE_SIZE,
    BATCH_SIZE
)
# -----------------------------
# Dataset Configuration
# -----------------------------

# IMAGE_SIZE = (128, 128)

# BATCH_SIZE = 32


# Dataset Path

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DATASET_PATH = os.path.join(BASE_DIR, "dataset", "chest_xray")

# TRAIN_PATH = os.path.join(DATASET_PATH, "train")

# VAL_PATH = os.path.join(DATASET_PATH, "val")

# TEST_PATH = os.path.join(DATASET_PATH, "test")


# -----------------------------
# Image Generators
# -----------------------------

train_datagen = ImageDataGenerator(

    rescale=1.0 / 255,

    rotation_range=40,

    width_shift_range=0.4,

    height_shift_range=0.4,

    shear_range=0.2,

    horizontal_flip=True,

    vertical_flip=True,

    fill_mode="nearest"

)

validation_datagen = ImageDataGenerator(

    rescale=1.0 / 255

)

test_datagen = ImageDataGenerator(

    rescale=1.0 / 255

)


# -----------------------------
# Data Loaders
# -----------------------------

train_generator = train_datagen.flow_from_directory(

    TRAIN_PATH,

    target_size=IMAGE_SIZE,

    batch_size=BATCH_SIZE,

    class_mode="categorical",

    shuffle=True

)

validation_generator = validation_datagen.flow_from_directory(

    VAL_PATH,

    target_size=IMAGE_SIZE,

    batch_size=BATCH_SIZE,

    class_mode="categorical",

    shuffle=False

)

test_generator = test_datagen.flow_from_directory(

    TEST_PATH,

    target_size=IMAGE_SIZE,

    batch_size=BATCH_SIZE,

    class_mode="categorical",

    shuffle=False

)


# -----------------------------
# Utility Function
# -----------------------------

def get_data_generators():

    """
    Returns train, validation and test generators.
    """

    return (

        train_generator,

        validation_generator,

        test_generator

    )