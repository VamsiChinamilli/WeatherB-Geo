"""
model_loader.py

Loads the ONNX Land-Cover model.
"""

import onnxruntime as ort

from app.services.huggingface.loader import HuggingFaceLoader


class ModelLoader:

    _session = None

    @classmethod
    def load_session(cls):

        if cls._session is not None:
            return cls._session

        model_path = HuggingFaceLoader.get_model_path()

        cls._session = ort.InferenceSession(
            model_path,
            providers=["CPUExecutionProvider"],
        )

        return cls._session