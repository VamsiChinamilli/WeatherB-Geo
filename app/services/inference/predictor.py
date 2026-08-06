"""
predictor.py

Runs Land-Cover ONNX inference.

Responsibilities
----------------
- Accept prepared model input.
- Run ONNX Runtime inference.
- Return raw logits.
"""

import numpy as np

from .model_loader import ModelLoader


class LandCoverPredictor:

    def __init__(self):

        self.session = ModelLoader.load_session()

        self.input_name = self.session.get_inputs()[0].name

        self.output_name = self.session.get_outputs()[0].name

    def predict(self, model_input):

        # Torch tensor -> NumPy (if necessary)
        if hasattr(model_input, "detach"):
            model_input = model_input.detach().cpu().numpy()

        model_input = np.asarray(
            model_input,
            dtype=np.float32,
        )

        logits = self.session.run(

            [self.output_name],

            {
                self.input_name: model_input
            }

        )[0]

        return logits