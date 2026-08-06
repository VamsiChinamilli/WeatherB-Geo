"""
tensor.py

Prepares the exact NumPy input expected by the
ONNX Land-Cover U-Net.

Final output

(1,5,256,256)
"""

import cv2
import numpy as np

from .normalize import (
    normalize_sentinel,
    normalize_thermal,
)

PATCH_SIZE = 256


# ---------------------------------------------------------
# Resize
# ---------------------------------------------------------

def resize_channels(image):
    """
    Resize image channel-wise.

    Input

        (C,H,W)

    Output

        (C,256,256)
    """

    if image.ndim != 3:
        raise ValueError(
            f"Expected (C,H,W), got {image.shape}"
        )

    resized = np.empty(
        (
            image.shape[0],
            PATCH_SIZE,
            PATCH_SIZE,
        ),
        dtype=np.float32,
    )

    for c in range(image.shape[0]):

        resized[c] = cv2.resize(

            image[c],

            (PATCH_SIZE, PATCH_SIZE),

            interpolation=cv2.INTER_LINEAR,

        )

    return resized


# ---------------------------------------------------------
# Sentinel
# ---------------------------------------------------------

def prepare_sentinel(sentinel):

    sentinel = normalize_sentinel(sentinel)

    return resize_channels(sentinel)


# ---------------------------------------------------------
# Thermal
# ---------------------------------------------------------

def prepare_thermal(thermal):

    thermal = normalize_thermal(thermal)

    thermal = np.expand_dims(
        thermal,
        axis=0,
    )

    return resize_channels(thermal)


# ---------------------------------------------------------
# Combined model input
# ---------------------------------------------------------

def build_model_input(
    sentinel,
    thermal,
):
    """
    Returns

        (1,5,256,256)

    float32
    """

    sentinel = prepare_sentinel(sentinel)

    thermal = prepare_thermal(thermal)

    combined = np.concatenate(

        [
            sentinel,
            thermal,
        ],

        axis=0,

    ).astype(np.float32)

    if combined.shape[0] != 5:

        raise RuntimeError(

            f"Expected 5 channels, got {combined.shape[0]}"

        )

    return np.expand_dims(
        combined,
        axis=0,
    )