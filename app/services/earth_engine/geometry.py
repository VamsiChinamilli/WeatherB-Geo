"""
geometry.py

Geometry helpers for Google Earth Engine.
"""

import ee

from .validator import validate_bbox


def geometry_from_bbox(bbox):
    """
    Convert bounding box into an Earth Engine rectangle.
    """

    validate_bbox(bbox)

    min_lon, min_lat, max_lon, max_lat = bbox

    return ee.Geometry.Rectangle(
        [
            min_lon,
            min_lat,
            max_lon,
            max_lat,
        ]
    )