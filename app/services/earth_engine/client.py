import ee

from .config import (
    PROJECT_ID,
    SERVICE_ACCOUNT,
    PRIVATE_KEY,
)


class EarthEngineClient:

    _initialized = False

    @classmethod
    def initialize(cls):

        if cls._initialized:
            return

        if SERVICE_ACCOUNT and PRIVATE_KEY:

            credentials = ee.ServiceAccountCredentials(
                SERVICE_ACCOUNT,
                key_data=PRIVATE_KEY,
            )

            ee.Initialize(
                credentials,
                project=PROJECT_ID,
            )

        else:

            ee.Initialize(project=PROJECT_ID)

        cls._initialized = True