"""
Shared utilities for Google Earth Engine providers.
"""

from datetime import datetime, timedelta

import ee


def validate_bbox(bbox):
    """
    Validate bounding box.

    Format:
        [min_lon, min_lat, max_lon, max_lat]
    """

    if bbox is None:
        raise ValueError("bbox cannot be None.")

    if len(bbox) != 4:
        raise ValueError(
            "bbox must be [min_lon, min_lat, max_lon, max_lat]."
        )

    min_lon, min_lat, max_lon, max_lat = bbox

    if min_lon >= max_lon:
        raise ValueError(
            "min_lon must be smaller than max_lon."
        )

    if min_lat >= max_lat:
        raise ValueError(
            "min_lat must be smaller than max_lat."
        )

    if not (
        -180 <= min_lon <= 180
        and -180 <= max_lon <= 180
        and -90 <= min_lat <= 90
        and -90 <= max_lat <= 90
    ):
        raise ValueError(
            "bbox coordinates are outside valid ranges."
        )


def geometry_from_bbox(bbox):
    """
    Convert bbox into Earth Engine geometry.
    """

    return ee.Geometry.Rectangle(
        [
            bbox[0],
            bbox[1],
            bbox[2],
            bbox[3],
        ]
    )


def date_range(days_back):
    """
    Return (start_date, end_date)
    """

    if days_back <= 0:
        raise ValueError(
            "days_back must be greater than zero."
        )

    end_date = datetime.utcnow()

    start_date = (
        end_date -
        timedelta(days=days_back)
    )

    return (
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d"),
    )