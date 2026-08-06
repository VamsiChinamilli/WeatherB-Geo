"""
landsat.py

Landsat thermal imagery service.

Responsibilities
----------------
- Search Landsat imagery
- Filter by bbox
- Filter by date
- Filter by cloud cover
- Return best scene
"""

import ee

from .config import LANDSAT_COLLECTION
from .common import date_range
from .geometry import geometry_from_bbox
from .validator import (
    validate_bbox,
    validate_cloud_limit,
    validate_days_back,
)


class LandsatService:
    """
    Service responsible for querying Landsat imagery.
    """

    def search(
        self,
        bbox,
        cloud_limit=20,
        days_back=90,
    ):
        """
        Search Landsat imagery.
        """

        validate_bbox(bbox)
        validate_cloud_limit(cloud_limit)
        validate_days_back(days_back)

        geometry = geometry_from_bbox(bbox)

        start_date, end_date = date_range(days_back)

        return (

            ee.ImageCollection(
                LANDSAT_COLLECTION
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
                    "CLOUD_COVER",
                    cloud_limit,
                )
            )

            .sort(
                "CLOUD_COVER"
            )

        )

    def get_best_scene(
        self,
        bbox,
        cloud_limit=20,
        days_back=90,
    ):
        """
        Return the least-cloudy Landsat scene.
        """

        collection = self.search(
            bbox=bbox,
            cloud_limit=cloud_limit,
            days_back=days_back,
        )

        if collection.size().getInfo() == 0:

            raise RuntimeError(
                "No suitable Landsat imagery found."
            )

        return ee.Image(
            collection.first()
        )