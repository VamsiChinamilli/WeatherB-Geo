"""
loader.py

Downloads the ONNX model repository from Hugging Face.
"""

from pathlib import Path

from huggingface_hub import snapshot_download

from app.config.config import (
    HF_REPO_ID,
    HF_MODEL_FILENAME,
)


class HuggingFaceLoader:

    MODEL_DIR = (
        Path(__file__).resolve().parents[3]
        / "models"
    )

    @classmethod
    def get_model_path(cls):

        cls.MODEL_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        model_path = cls.MODEL_DIR / HF_MODEL_FILENAME

        if model_path.exists():
            return model_path

        snapshot_download(

            repo_id=HF_REPO_ID,

            local_dir=cls.MODEL_DIR,

            local_dir_use_symlinks=False,

        )

        return model_path