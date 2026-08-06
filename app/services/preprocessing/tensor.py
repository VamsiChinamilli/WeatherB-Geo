"""
tensor.py

Tensor preparation utilities.

Converts normalized NumPy arrays into the exact tensor
expected by the trained U-Net.

Final output:

(1,5,256,256)
"""

import torch
import torch.nn.functional as F

from .normalize import (
    normalize_sentinel,
    normalize_thermal,
)


PATCH_SIZE = 256


# ---------------------------------------------------------
# Resize
# ---------------------------------------------------------

def resize_tensor(tensor):
    """
    Resize tensor.

    Input

        (C,H,W)

    Output

        (C,256,256)
    """

    if tensor.ndim != 3:
        raise ValueError(
            f"Expected tensor (C,H,W), got {tensor.shape}"
        )

    tensor = tensor.unsqueeze(0)

    tensor = F.interpolate(
        tensor,
        size=(
            PATCH_SIZE,
            PATCH_SIZE,
        ),
        mode="bilinear",
        align_corners=False,
    )

    return tensor.squeeze(0)


# ---------------------------------------------------------
# Sentinel
# ---------------------------------------------------------

def prepare_sentinel(sentinel):
    """
    Prepare Sentinel tensor.

    Returns

        (4,256,256)
    """

    sentinel = normalize_sentinel(sentinel)

    tensor = torch.from_numpy(
        sentinel
    ).float()

    return resize_tensor(tensor)


# ---------------------------------------------------------
# Thermal
# ---------------------------------------------------------

def prepare_thermal(thermal):
    """
    Prepare thermal tensor.

    Returns

        (1,256,256)
    """

    thermal = normalize_thermal(thermal)

    tensor = torch.from_numpy(
        thermal
    ).float()

    tensor = tensor.unsqueeze(0)

    return resize_tensor(tensor)


# ---------------------------------------------------------
# Combined model input
# ---------------------------------------------------------

def build_model_input(
    sentinel,
    thermal,
):
    """
    Build the exact input expected by the U-Net.

    Channel order

        0 B4
        1 B3
        2 B2
        3 B8
        4 Thermal

    Returns

        (1,5,256,256)
    """

    sentinel_tensor = prepare_sentinel(
        sentinel
    )

    thermal_tensor = prepare_thermal(
        thermal
    )

    combined = torch.cat(
        [
            sentinel_tensor,
            thermal_tensor,
        ],
        dim=0,
    )

    if combined.shape[0] != 5:
        raise RuntimeError(
            f"Expected 5 channels, got {combined.shape[0]}"
        )

    return combined.unsqueeze(0)