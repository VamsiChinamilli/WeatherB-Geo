"""
routes.py

FastAPI routes for WeatherB-AI.
"""

from fastapi import APIRouter, HTTPException

from app.schemas.request import AnalyzeRequest
from app.schemas.response import AnalyzeResponse

from app.services.earth_engine.provider import EarthEngineProvider

from app.services.preprocessing.tensor import (
    build_model_input,
)

from app.services.inference.predictor import (
    LandCoverPredictor,
)

from app.services.inference.postprocess import (
    PredictionPostProcessor,
)

from app.services.expert_system.landcover import (
    LandCoverExpertSystem,
)

from app.services.expert_system.lst import (
    LSTExpertSystem,
)

router = APIRouter(
    prefix="/api",
    tags=["WeatherB-AI"],
)

# ----------------------------------------------------------
# Create services once
# ----------------------------------------------------------

provider = EarthEngineProvider()

predictor = LandCoverPredictor()

landcover_expert = LandCoverExpertSystem()

lst_expert = LSTExpertSystem()


# ----------------------------------------------------------
# Analyze endpoint
# ----------------------------------------------------------

@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
)
def analyze(
    request: AnalyzeRequest,
):

    try:

        # ------------------------------------------
        # Download imagery
        # ------------------------------------------

        climate = provider.get_climate_data(
            request.bbox
        )

        sentinel = climate["sentinel"]["bands"]

        thermal = climate["thermal"]["thermal"]

        # ------------------------------------------
        # Build model tensor
        # ------------------------------------------

        model_input = build_model_input(
            sentinel,
            thermal,
        )

        # ------------------------------------------
        # UNet inference
        # ------------------------------------------

        logits = predictor.predict(
            model_input
        )

        # ------------------------------------------
        # Postprocess
        # ------------------------------------------

        prediction = (
            PredictionPostProcessor.process(
                logits
            )
        )

        # ------------------------------------------
        # Expert systems
        # ------------------------------------------

        landcover = (
            landcover_expert.analyze(
                prediction["land_cover"]
            )
        )

        lst = lst_expert.estimate(
            landcover=landcover
        )

        # ------------------------------------------
        # Final response
        # ------------------------------------------

        return AnalyzeResponse(

            bbox=request.bbox,

            land_cover=landcover,

            lst=lst,

        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )