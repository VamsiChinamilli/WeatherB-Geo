"""
predictor.py

Runs Land-Cover U-Net inference.

Responsibilities
----------------
- Accept a prepared tensor.
- Run the model.
- Compute probabilities.
- Compute segmentation mask.
"""

import torch

from .model_loader import ModelLoader


class LandCoverPredictor:

    def __init__(self):

        self.model = ModelLoader.load_unet()

        self.device = ModelLoader.DEVICE

    @torch.no_grad()
    def predict(self, model_input):

        model_input = model_input.to(self.device)

        logits = self.model(model_input)

        return logits