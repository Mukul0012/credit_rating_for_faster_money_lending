from pathlib import Path

import joblib


BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "random_forest_tuned.pkl"
)

ENCODER_PATH = (
    BASE_DIR
    / "models"
    / "encoder.pkl"
)


class ModelLoader:

    _model = None
    _encoder = None

    @classmethod
    def get_model(cls):

        if cls._model is None:

            if not MODEL_PATH.exists():

                raise FileNotFoundError(
                    f"Random Forest model not found: "
                    f"{MODEL_PATH}"
                )

            cls._model = joblib.load(
                MODEL_PATH
            )

        return cls._model

    @classmethod
    def get_encoder(cls):

        if cls._encoder is None:

            if not ENCODER_PATH.exists():

                raise FileNotFoundError(
                    f"Encoder not found: "
                    f"{ENCODER_PATH}"
                )

            cls._encoder = joblib.load(
                ENCODER_PATH
            )

        return cls._encoder