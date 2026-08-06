"""
loader.py

Downloads the trained model from Hugging Face
only once.

Responsibilities
----------------
- Download weights_only.pth if missing.
- Cache locally.
- Return local model path.
"""

from pathlib import Path

from huggingface_hub import hf_hub_download

from app.config.config import (
    HF_REPO_ID,
    HF_MODEL_FILENAME,
)


class HuggingFaceLoader:

    MODEL_DIR = (
        Path(__file__).resolve().parents[3]
        / "models"
    )

    MODEL_PATH = MODEL_DIR / HF_MODEL_FILENAME

    @classmethod
    def get_model_path(cls):
        """
        Returns the local path to the model.

        Downloads it only once if necessary.
        """

        cls.MODEL_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        if cls.MODEL_PATH.exists():
            return cls.MODEL_PATH

        downloaded = hf_hub_download(

            repo_id=HF_REPO_ID,

            filename=HF_MODEL_FILENAME,

            local_dir=cls.MODEL_DIR,

            local_dir_use_symlinks=False,

        )

        return Path(downloaded)