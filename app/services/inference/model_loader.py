"""
model_loader.py

Loads the trained Land-Cover U-Net.
"""

import torch

from app.models.model import UNet
from app.services.huggingface.loader import HuggingFaceLoader


class ModelLoader:

    _model = None

    DEVICE = torch.device("cpu")

    @classmethod
    def load_unet(cls):

        if cls._model is not None:
            return cls._model

        # Download from Hugging Face if needed
        model_path = HuggingFaceLoader.get_model_path()

        model = UNet(
            in_channels=5,
            num_classes=11,
            pretrained=False,
        )

        state_dict = torch.load(
            model_path,
            map_location=cls.DEVICE,
            weights_only=True,
        )

        model.load_state_dict(state_dict)

        model.to(cls.DEVICE)

        model.eval()

        cls._model = model

        return cls._model