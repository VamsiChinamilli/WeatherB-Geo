"""
WeatherB-AI

FastAPI entrypoint.
"""

from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(

    title="WeatherB-AI",

    version="1.0.0",

    description=(
        "AI inference service for the "
        "GeospatialAI platform."
    ),
)

app.include_router(router)


@app.get("/")
def root():

    return {

        "service": "WeatherB-AI",

        "status": "running",

        "docs": "/docs",

    }