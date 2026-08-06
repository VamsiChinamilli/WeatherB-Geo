"""
postprocess.py

Post-processing utilities for the Land-Cover U-Net.

Responsibilities
----------------
- Convert logits into probabilities.
- Generate segmentation masks.
- Calculate land-cover percentages.
- Produce JSON-friendly outputs.

This module does NOT:
- Load the model.
- Perform inference.
- Handle HTTP requests.
"""

import numpy as np
import torch


# ---------------------------------------------------------
# Land-cover class names
# ---------------------------------------------------------

LAND_COVER_CLASSES = {

0: "Tree Cover",
1: "Shrubland",
2: "Grassland",
3: "Cropland",
4: "Built-up",
5: "Bare / Sparse Vegetation",
6: "Snow and Ice",
7: "Permanent Water Bodies",
8: "Herbaceous Wetland",
9: "Mangroves",
10: "Moss and Lichen",

}


class PredictionPostProcessor:
    """
    Post-process raw U-Net predictions.
    """

    @staticmethod
    def probabilities(logits):
        """
        Convert logits to probabilities.

        Parameters
        ----------
        logits : Tensor

            (1,11,H,W)

        Returns
        -------
        Tensor
        """

        return torch.softmax(
            logits,
            dim=1,
        )

    @staticmethod
    def segmentation_mask(probabilities):
        """
        Create segmentation mask.

        Returns

            (H,W)
        """

        return torch.argmax(
            probabilities,
            dim=1,
        ).squeeze(0)

    @staticmethod
    def class_percentages(mask):
        """
        Calculate percentage occupied by
        every land-cover class.
        """

        if isinstance(mask, torch.Tensor):
            mask = mask.cpu().numpy()

        total_pixels = mask.size

        percentages = {}

        unique, counts = np.unique(
            mask,
            return_counts=True,
        )

        for class_id, count in zip(unique, counts):

            percentages[
                LAND_COVER_CLASSES.get(
                    int(class_id),
                    f"Class {class_id}",
                )
            ] = round(
                float(count) * 100.0 / total_pixels,
                2,
            )

        return percentages

    @staticmethod
    def to_numpy(tensor):
        """
        Convert tensor to NumPy.
        """

        if isinstance(
            tensor,
            torch.Tensor,
        ):
            return tensor.detach().cpu().numpy()

        return tensor

    @classmethod
    def process(cls, logits):
        """
        Complete post-processing pipeline.

        Parameters
        ----------
        logits

            (1,11,H,W)

        Returns
        -------
        dict
        """

        probabilities = cls.probabilities(
            logits
        )

        mask = cls.segmentation_mask(
            probabilities
        )

        percentages = cls.class_percentages(
            mask
        )

        return {

            "logits":
                cls.to_numpy(logits),

            "probabilities":
                cls.to_numpy(probabilities),

            "mask":
                cls.to_numpy(mask),

            "land_cover":
                percentages,

        }