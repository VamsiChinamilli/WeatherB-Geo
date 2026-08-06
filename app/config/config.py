"""
Application configuration.

Central location for all configurable settings used by
the WeatherB-AI service.
"""

import os
from dotenv import load_dotenv

load_dotenv()


# ==========================================================
# Hugging Face
# ==========================================================

HF_REPO_ID = os.getenv(
    "HF_REPO_ID",
    "naga-vamsi/weatherb-landcover-unet",
)

HF_MODEL_FILENAME = os.getenv(
    "HF_MODEL_FILENAME",
    "weights_only.pth",
)


# ==========================================================
# Google Earth Engine
# ==========================================================

GEE_SERVICE_ACCOUNT = os.getenv("GEE_SERVICE_ACCOUNT")

GEE_PRIVATE_KEY = os.getenv("GEE_PRIVATE_KEY")


# ==========================================================
# Model
# ==========================================================

PATCH_SIZE = 256

NUM_CLASSES = 11

INPUT_CHANNELS = 5


# ==========================================================
# Raster
# ==========================================================

SENTINEL_SCALE = 10

LANDSAT_SCALE = 30