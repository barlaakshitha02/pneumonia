import os

from tensorflow.keras.callbacks import (
    EarlyStopping,
    ModelCheckpoint,
    ReduceLROnPlateau
)

from data_loader import get_data_generators
from model import build_model
from config import MODEL_DIR, MODEL_PATH, EPOCHS


# ===========================================
# Create Model Folder
# ===========================================

os.makedirs(MODEL_DIR, exist_ok=True)


# ===========================================
# Load Dataset
# ===========================================

train_generator, validation_generator, test_generator = get_data_generators()


# ===========================================
# Build Model
# ===========================================

model = build_model()

model.summary()


# ===========================================
# Callbacks
# ===========================================

early_stopping = EarlyStopping(

    monitor="val_loss",

    patience=4,

    restore_best_weights=True,

    verbose=1

)

checkpoint = ModelCheckpoint(

    MODEL_PATH,

    monitor="val_accuracy",

    save_best_only=True,

    verbose=1

)

reduce_lr = ReduceLROnPlateau(

    monitor="val_loss",

    factor=0.5,

    patience=2,

    min_lr=1e-6,

    verbose=1

)


# ===========================================
# Train Model
# ===========================================

history = model.fit(

    train_generator,

    validation_data=validation_generator,

    epochs=EPOCHS,

    callbacks=[

        early_stopping,

        checkpoint,

        reduce_lr

    ]

)


# ===========================================
# Save Final Model
# ===========================================

model.save(MODEL_PATH)

print("\n====================================")
print("✅ Training Completed Successfully")
print(f"Model Saved At:\n{MODEL_PATH}")
print("====================================")