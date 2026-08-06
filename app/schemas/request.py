"""
request.py

Pydantic request models for WeatherB-AI.
"""

from pydantic import BaseModel, Field, field_validator


class AnalyzeRequest(BaseModel):
    """
    Bounding box supplied by WeatherB-Core.

    Format

        [min_lon, min_lat, max_lon, max_lat]
    """

    bbox: list[float] = Field(
        ...,
        min_length=4,
        max_length=4,
        description="Bounding box [min_lon, min_lat, max_lon, max_lat]",
    )

    @field_validator("bbox")
    @classmethod
    def validate_bbox(cls, bbox):

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
            and
            -180 <= max_lon <= 180
            and
            -90 <= min_lat <= 90
            and
            -90 <= max_lat <= 90
        ):
            raise ValueError(
                "Invalid longitude/latitude."
            )

        return bbox