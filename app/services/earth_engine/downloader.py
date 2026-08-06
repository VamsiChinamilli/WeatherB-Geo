"""
downloader.py

Download Earth Engine imagery directly into NumPy arrays.

Responsibilities
----------------
- Generate download URLs
- Download raster bytes
- Convert to NumPy
- Never write temporary files
"""

from io import BytesIO

import ee
import numpy as np
import requests


class RasterDownloader:
    """
    Downloads Earth Engine rasters into memory.
    """

    @staticmethod
    def download(
        image,
        bbox,
        bands,
        scale,
    ):
        """
        Download an Earth Engine image region as NumPy.
        """

        geometry = ee.Geometry.Rectangle(bbox)

        url = image.getDownloadURL(
            {
                "bands": bands,
                "region": geometry,
                "scale": scale,
                "format": "NPY",
            }
        )

        response = requests.get(
            url,
            timeout=300,
        )

        response.raise_for_status()

        data = np.load(
            BytesIO(response.content)
        )

        return data

    @staticmethod
    def structured_to_array(
        data,
        band_name=None,
    ):
        """
        Convert structured NPY into ndarray.
        """

        if data.dtype.names:

            if band_name is None:
                return np.stack(
                    [
                        data[name]
                        for name in data.dtype.names
                    ],
                    axis=0,
                )

            return data[band_name]

        if data.ndim == 3:
            return data

        if data.ndim == 2:
            return data

        raise RuntimeError(
            "Unexpected raster dimensions."
        )