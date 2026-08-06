"""
landcover.py

Land-cover interpretation layer.

Responsibilities
----------------
- Interpret U-Net output.
- Compute high-level land-cover metrics.
- Identify dominant land-cover.
- Produce JSON-friendly analysis.

Does NOT:
- Run U-Net.
- Download imagery.
- Predict temperature.
"""

from typing import Dict


class LandCoverExpertSystem:

    VEGETATION_CLASSES = {
    "Tree Cover",
    "Shrubland",
    "Grassland",
    "Cropland",
    "Mangroves",
    "Herbaceous Wetland",
}

    BUILT_CLASSES = {
    "Built-up",
}

    WATER_CLASSES = {
    "Permanent Water Bodies",
}

    BARREN_CLASSES = {
    "Bare / Sparse Vegetation",
}

    def analyze(
        self,
        class_percentages: Dict[str, float],
    ) -> Dict:

        if not class_percentages:
            raise ValueError(
                "class_percentages cannot be empty."
            )

        dominant = max(
            class_percentages,
            key=class_percentages.get,
        )

        vegetation = sum(
            class_percentages.get(c, 0.0)
            for c in self.VEGETATION_CLASSES
        )

        built = sum(
            class_percentages.get(c, 0.0)
            for c in self.BUILT_CLASSES
        )

        water = sum(
            class_percentages.get(c, 0.0)
            for c in self.WATER_CLASSES
        )

        barren = sum(
            class_percentages.get(c, 0.0)
            for c in self.BARREN_CLASSES
        )

        return {

            "dominant_class": dominant,

            "vegetation_percent": round(
                vegetation,
                2,
            ),

            "built_percent": round(
                built,
                2,
            ),

            "water_percent": round(
                water,
                2,
            ),

            "barren_percent": round(
                barren,
                2,
            ),

            "class_percentages": class_percentages,
        }