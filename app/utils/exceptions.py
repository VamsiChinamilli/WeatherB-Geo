"""
exceptions.py

Custom exceptions for WeatherB-AI.
"""


class WeatherAIException(Exception):
    """
    Base exception.
    """
    pass


class EarthEngineException(
    WeatherAIException
):
    """
    Earth Engine download failure.
    """
    pass


class RasterException(
    WeatherAIException
):
    """
    Raster processing failure.
    """
    pass


class ModelLoadingException(
    WeatherAIException
):
    """
    Model loading failure.
    """
    pass


class InferenceException(
    WeatherAIException
):
    """
    U-Net inference failure.
    """
    pass


class ExpertSystemException(
    WeatherAIException
):
    """
    Expert system failure.
    """
    pass