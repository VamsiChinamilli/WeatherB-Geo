"""
response.py

Pydantic response models for WeatherB-AI.
"""

from typing import Dict, List

from pydantic import BaseModel


# ---------------------------------------------------------
# LST Models
# ---------------------------------------------------------

class TemperatureRange(BaseModel):

    min: float

    max: float


class Contributor(BaseModel):

    class_name: str

    effect_celsius: float

    direction: str


class TemperaturePrediction(BaseModel):

    estimated_lst_celsius: float

    expected_range_celsius: TemperatureRange

    classification: str

    confidence: float

    baseline_temperature: float

    land_cover_effects: Dict[str, float]

    environmental_effects: Dict[str, float]

    total_land_cover_effect: float

    total_environmental_effect: float

    main_contributors: List[Contributor]


# ---------------------------------------------------------
# Land Cover
# ---------------------------------------------------------

class LandCoverAnalysis(BaseModel):

    dominant_class: str

    vegetation_percent: float

    built_percent: float

    water_percent: float

    barren_percent: float

    class_percentages: Dict[str, float]


# ---------------------------------------------------------
# Final Response
# ---------------------------------------------------------

class AnalyzeResponse(BaseModel):

    bbox: list[float]

    land_cover: LandCoverAnalysis

    lst: TemperaturePrediction