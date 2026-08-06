"""
sentinel.py

Sentinel-2 imagery service.

Responsibilities
----------------
- Search Sentinel-2 imagery
- Filter by bbox
- Filter by date
- Filter by cloud percentage
- Return the best scene
"""

import ee

from .config import SENTINEL_COLLECTION
from .common import date_range
from .geometry import geometry_from_bbox
from .validator import (
    validate_bbox,
    validate_cloud_limit,
    validate_days_back,
)


class SentinelService:
    """
    Service responsible for querying Sentinel-2 imagery.
    """

    def search(
        self,
        bbox,
        cloud_limit=10,
        days_back=90,
    ):
        """
        Search Sentinel-2 imagery.
        """

        validate_bbox(bbox)
        validate_cloud_limit(cloud_limit)
        validate_days_back(days_back)

        geometry = geometry_from_bbox(bbox)

        start_date, end_date = date_range(days_back)

        return (

            ee.ImageCollection(
                SENTINEL_COLLECTION
            )

            .filterBounds(
                geometry
            )

            .filterDate(
                start_date,
                end_date,
            )

            .filter(
                ee.Filter.lt(
                    "CLOUDY_PIXEL_PERCENTAGE",
                    cloud_limit,
                )
            )

            .sort(
                "CLOUDY_PIXEL_PERCENTAGE"
            )

        )

    def get_best_scene(
        self,
        bbox,
        cloud_limit=10,
        days_back=90,
    ):
        """
        Return the least-cloudy Sentinel scene.
        """

        collection = self.search(
            bbox=bbox,
            cloud_limit=cloud_limit,
            days_back=days_back,
        )

        if collection.size().getInfo() == 0:

            raise RuntimeError(
                "No suitable Sentinel-2 imagery found."
            )

        return ee.Image(
            collection.first()
        )