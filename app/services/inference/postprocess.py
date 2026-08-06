"""
postprocess.py

Post-processing utilities for the Land-Cover ONNX model.

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
    Post-process raw ONNX predictions.
    """

    @staticmethod
    def probabilities(logits):
        """
        Convert logits into softmax probabilities.

        Parameters
        ----------
        logits : ndarray

            Shape:
                (1, 11, H, W)

        Returns
        -------
        ndarray

            Shape:
                (1, 11, H, W)
        """

        logits = np.asarray(
            logits,
            dtype=np.float32,
        )

        # Numerically stable softmax
        logits = logits - np.max(
            logits,
            axis=1,
            keepdims=True,
        )

        exp = np.exp(logits)

        probabilities = exp / np.sum(
            exp,
            axis=1,
            keepdims=True,
        )

        return probabilities

    @staticmethod
    def segmentation_mask(probabilities):
        """
        Create segmentation mask.

        Returns
        -------
        ndarray

            Shape:
                (H, W)
        """

        return np.argmax(
            probabilities,
            axis=1,
        ).squeeze(0)

    @staticmethod
    def class_percentages(mask):
        """
        Calculate percentage occupied by
        every land-cover class.
        """

        mask = np.asarray(
            mask,
            dtype=np.int64,
        )

        total_pixels = mask.size

        percentages = {}

        unique, counts = np.unique(
            mask,
            return_counts=True,
        )

        for class_id, count in zip(unique, counts):

            class_name = LAND_COVER_CLASSES.get(
                int(class_id),
                f"Class {class_id}",
            )

            percentages[class_name] = round(
                float(count) * 100.0 / total_pixels,
                2,
            )

        return percentages

    @staticmethod
    def to_numpy(array):
        """
        Ensure output is a NumPy array.
        """

        return np.asarray(array)

    @classmethod
    def process(cls, logits):
        """
        Complete post-processing pipeline.

        Parameters
        ----------
        logits

            Shape:
                (1, 11, H, W)

        Returns
        -------
        dict
        """

        logits = cls.to_numpy(logits)

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
                logits,

            "probabilities":
                probabilities,

            "mask":
                mask,

            "land_cover":
                percentages,

        }