"""
lst.py

Rule-based Land Surface Temperature Expert System.

Uses land-cover composition to estimate
realistic urban surface temperatures.
"""

from typing import Dict, Any


class LSTExpertSystem:

    BASE_TEMPERATURE = 30.0

    LAND_COVER_EFFECTS = {

        "Built-up": 0.10,

        "Tree Cover": -0.06,

        "Permanent Water Bodies": -0.08,

        "Cropland": -0.03,

        "Grassland": -0.03,

        "Shrubland": -0.04,

        "Mangroves": -0.06,

        "Herbaceous Wetland": -0.05,

        "Bare / Sparse Vegetation": 0.04,

    }

    DEFAULT_ENVIRONMENT = {

        "season": 1.5,

        "solar": 0.8,

        "vegetation": -0.3,

    }

    RANGE_MARGIN = 1.5

    def estimate(

        self,

        landcover,

        environment=None,

    ) -> Dict[str, Any]:

        class_percentages = landcover["class_percentages"]

        if environment is None:

            environment = self.DEFAULT_ENVIRONMENT

        land_cover_effects = {}

        total_land_effect = 0.0

        for cls, percentage in class_percentages.items():

            coefficient = self.LAND_COVER_EFFECTS.get(cls, 0.0)

            effect = percentage * coefficient

            land_cover_effects[cls] = round(effect, 2)

            total_land_effect += effect

        environmental_effects = {

            "season": float(environment.get("season", 1.5)),

            "solar": float(environment.get("solar", 0.8)),

            "vegetation": float(environment.get("vegetation", -0.3)),

        }

        total_environment = sum(

            environmental_effects.values()

        )

        estimated = (

            self.BASE_TEMPERATURE

            + total_land_effect

            + total_environment

        )

        confidence = 0.85

        total_percent = sum(class_percentages.values())

        if total_percent < 80:

            confidence = 0.70

        if estimated > 45:

            confidence -= 0.10

        if estimated < 15:

            confidence -= 0.10

        confidence = max(0.5, min(confidence, 0.95))

        if estimated < 20:

            classification = "Cool"

        elif estimated < 27:

            classification = "Moderate"

        elif estimated < 35:

            classification = "Warm"

        elif estimated < 42:

            classification = "Hot"

        else:

            classification = "Very Hot"

        contributors = sorted(

            land_cover_effects.items(),

            key=lambda x: abs(x[1]),

            reverse=True,

        )[:5]

        contributors = [

    {

        "class_name": c,

        "effect_celsius": round(v, 2),

        "direction":

            "warming"

            if v > 0

            else "cooling"

            if v < 0

            else "neutral",

    }

            for c, v in contributors

]

        return {

            "estimated_lst_celsius":

                round(estimated, 2),

            "expected_range_celsius": {

                "min":

                    round(

                        estimated - self.RANGE_MARGIN,

                        2,

                    ),

                "max":

                    round(

                        estimated + self.RANGE_MARGIN,

                        2,

                    ),

            },

            "classification":

                classification,

            "confidence":

                round(confidence, 2),

            "baseline_temperature":

                self.BASE_TEMPERATURE,

            "land_cover_effects":

                land_cover_effects,

            "environmental_effects":

                environmental_effects,

            "total_land_cover_effect":

                round(total_land_effect, 2),

            "total_environmental_effect":

                round(total_environment, 2),

            "main_contributors":

                contributors,

        }