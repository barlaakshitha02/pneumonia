from tensorflow.keras.applications import VGG19
from tensorflow.keras.layers import Flatten, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import SGD


def build_model():

    """
    Builds the VGG19 Pneumonia Detection Model.
    """

    # -----------------------------
    # Load Pre-trained VGG19
    # -----------------------------

    base_model = VGG19(

        include_top=False,

        weights="imagenet",

        input_shape=(128, 128, 3)

    )

    # Freeze all convolutional layers

    for layer in base_model.layers:

        layer.trainable = False

    # -----------------------------
    # Custom Classification Head
    # -----------------------------

    x = base_model.output

    x = Flatten()(x)

    x = Dense(4608, activation="relu")(x)

    x = Dropout(0.2)(x)

    x = Dense(1152, activation="relu")(x)

    predictions = Dense(2, activation="softmax")(x)

    model = Model(

        inputs=base_model.input,

        outputs=predictions

    )

    # -----------------------------
    # Compile Model
    # -----------------------------

    optimizer = SGD(

        learning_rate=0.0001,

        momentum=0.0,

        nesterov=True

    )

    model.compile(

        optimizer=optimizer,

        loss="categorical_crossentropy",

        metrics=["accuracy"]

    )

    return model