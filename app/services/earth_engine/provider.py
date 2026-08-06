"""
provider.py

Public interface for retrieving climate imagery.

Responsibilities
----------------
- Retrieve Sentinel imagery
- Retrieve Landsat thermal imagery
- Download rasters
- Return unified climate inputs
"""

from .config import (
    SENTINEL_BANDS,
    THERMAL_BAND,
)
from .client import EarthEngineClient
from .downloader import RasterDownloader

from .landsat import LandsatService
from .sentinel import SentinelService


class EarthEngineProvider:
    """
    High-level Earth Engine provider.
    """

    def __init__(self):
        EarthEngineClient.initialize()


        self.sentinel = SentinelService()

        self.landsat = LandsatService()

        self.downloader = RasterDownloader()

    def get_sentinel_data(
        self,
        bbox,
        cloud_limit=10,
        days_back=90,
        scale=10,
    ):

        scene = self.sentinel.get_best_scene(
            bbox=bbox,
            cloud_limit=cloud_limit,
            days_back=days_back,
        )

        raster = self.downloader.download(
            image=scene,
            bbox=bbox,
            bands=SENTINEL_BANDS,
            scale=scale,
        )

        raster = self.downloader.structured_to_array(
            raster
        )

        return {

            "scene": scene,

            "bands": raster,

            "metadata": {

                "sensor": "Sentinel-2",

                "resolution": scale,

                "bands": SENTINEL_BANDS,

            },

        }

    def get_thermal_data(
        self,
        bbox,
        cloud_limit=20,
        days_back=90,
        scale=30,
    ):

        scene = self.landsat.get_best_scene(
            bbox=bbox,
            cloud_limit=cloud_limit,
            days_back=days_back,
        )

        thermal_image = (

            scene

            .select(
                THERMAL_BAND
            )

            .multiply(
                0.00341802
            )

            .add(
                149.0
            )

            .rename(
                "temperature"
            )

        )

        raster = self.downloader.download(
            image=thermal_image,
            bbox=bbox,
            bands=["temperature"],
            scale=scale,
        )

        raster = self.downloader.structured_to_array(
            raster,
            "temperature",
        )

        return {

            "scene": scene,

            "thermal": raster,

            "metadata": {

                "sensor": "Landsat-8",

                "resolution": scale,

                "unit": "Kelvin",

            },

        }

    def get_climate_data(
        self,
        bbox,
    ):
        """
        Retrieve all imagery required by the AI pipeline.
        """

        sentinel = self.get_sentinel_data(
            bbox=bbox,
        )

        thermal = self.get_thermal_data(
            bbox=bbox,
        )

        return {

            "bbox": bbox,

            "sentinel": sentinel,

            "thermal": thermal,

        }