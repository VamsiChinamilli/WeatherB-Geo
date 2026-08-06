"""
normalize.py

Normalization utilities used by the AI pipeline.

These functions reproduce exactly the preprocessing
used while training the Land-Cover U-Net.

Nothing here performs resizing or tensor conversion.
"""

import numpy as np


# ---------------------------------------------------------
# Sentinel
# ---------------------------------------------------------

REQUIRED_SENTINEL_BANDS = (
    "B4",
    "B3",
    "B2",
    "B8",
)


def normalize_sentinel(sentinel):
    """
    Normalize Sentinel imagery.

    Input may be either:

        structured array

    or

        ndarray with shape (4,H,W)

    Returns

        ndarray (4,H,W)
        float32
    """

    if getattr(sentinel.dtype, "names", None):

        for band in REQUIRED_SENTINEL_BANDS:

            if band not in sentinel.dtype.names:
                raise ValueError(
                    f"Missing Sentinel band: {band}"
                )

        sentinel = np.stack(
            [
                sentinel["B4"],
                sentinel["B3"],
                sentinel["B2"],
                sentinel["B8"],
            ],
            axis=0,
        )

    else:

        sentinel = np.asarray(sentinel)

    if sentinel.ndim != 3:
        raise ValueError(
            f"Expected Sentinel shape (4,H,W), got {sentinel.shape}"
        )

    if sentinel.shape[0] != 4:
        raise ValueError(
            f"Expected 4 Sentinel channels, got {sentinel.shape[0]}"
        )

    sentinel = sentinel.astype(np.float32)

    sentinel /= 10000.0

    sentinel = np.clip(
        sentinel,
        0.0,
        1.0,
    )

    return sentinel


# ---------------------------------------------------------
# Thermal
# ---------------------------------------------------------

def normalize_thermal(thermal):
    """
    Normalize Landsat thermal image.

    Training normalization:

        clip(250,350)

        (thermal-250)/100

    Returns

        ndarray (H,W)
    """

    thermal = np.asarray(
        thermal,
        dtype=np.float32,
    )

    if thermal.ndim == 3:

        if thermal.shape[0] == 1:
            thermal = thermal[0]
        else:
            raise ValueError(
                "Thermal raster must contain one channel."
            )

    if thermal.ndim != 2:
        raise ValueError(
            f"Expected thermal shape (H,W), got {thermal.shape}"
        )

    thermal = np.clip(
        thermal,
        250.0,
        350.0,
    )

    thermal = (
        thermal - 250.0
    ) / 100.0

    return thermal.astype(np.float32)