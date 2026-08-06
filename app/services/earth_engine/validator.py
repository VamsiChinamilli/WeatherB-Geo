"""
validator.py

Validation helpers for the Earth Engine module.

These functions validate user inputs before any
Google Earth Engine request is made.
"""


def validate_bbox(bbox):
    """
    Validate bounding box.

    Expected format:
        [min_lon, min_lat, max_lon, max_lat]
    """

    if bbox is None:
        raise ValueError("Bounding box cannot be None.")

    if not isinstance(bbox, (list, tuple)):
        raise TypeError(
            "Bounding box must be a list or tuple."
        )

    if len(bbox) != 4:
        raise ValueError(
            "Bounding box must contain exactly four coordinates."
        )

    min_lon, min_lat, max_lon, max_lat = bbox

    for coordinate in bbox:

        if not isinstance(
            coordinate,
            (int, float),
        ):
            raise TypeError(
                "Bounding box coordinates must be numeric."
            )

    if min_lon >= max_lon:
        raise ValueError(
            "Minimum longitude must be smaller than maximum longitude."
        )

    if min_lat >= max_lat:
        raise ValueError(
            "Minimum latitude must be smaller than maximum latitude."
        )

    if not (-180 <= min_lon <= 180):
        raise ValueError("Invalid minimum longitude.")

    if not (-180 <= max_lon <= 180):
        raise ValueError("Invalid maximum longitude.")

    if not (-90 <= min_lat <= 90):
        raise ValueError("Invalid minimum latitude.")

    if not (-90 <= max_lat <= 90):
        raise ValueError("Invalid maximum latitude.")


def validate_cloud_limit(limit):
    """
    Validate cloud percentage.
    """

    if not isinstance(limit, (int, float)):
        raise TypeError(
            "Cloud limit must be numeric."
        )

    if not (0 <= limit <= 100):
        raise ValueError(
            "Cloud limit must be between 0 and 100."
        )


def validate_days_back(days_back):
    """
    Validate search window.
    """

    if not isinstance(days_back, int):
        raise TypeError(
            "days_back must be an integer."
        )

    if days_back <= 0:
        raise ValueError(
            "days_back must be greater than zero."
        )


def validate_scale(scale):
    """
    Validate raster resolution.
    """

    if not isinstance(scale, (int, float)):
        raise TypeError(
            "Scale must be numeric."
        )

    if scale <= 0:
        raise ValueError(
            "Scale must be greater than zero."
        )