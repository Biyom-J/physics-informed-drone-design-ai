import random
import copy


def enforce_constraints(
        design,
        mission
):

    payload = mission["payload_kg"]

    # Weight must be greater than payload
    if design.get(
            "estimated_weight_kg",
            0
    ) < payload:

        design["estimated_weight_kg"] = round(
            payload * random.uniform(
                1.8,
                2.5
            ),
            2
        )

    # Aerodynamic limits
    if "drag_coefficient" in design:

        design["drag_coefficient"] = min(
            max(
                design["drag_coefficient"],
                0.03
            ),
            0.15
        )

    if "wing_area_m2" in design:

        design["wing_area_m2"] = min(
            max(
                design["wing_area_m2"],
                0.3
            ),
            3.0
        )

    if "propeller_diameter_inch" in design:

        design["propeller_diameter_inch"] = min(
            max(
                design["propeller_diameter_inch"],
                12
            ),
            40
        )

    # Propulsion limits
    if "battery_mAh" in design:

        design["battery_mAh"] = int(
            min(
                max(
                    design["battery_mAh"],
                    5000
                ),
                50000
            )
        )

    if "motor_KV" in design:

        design["motor_KV"] = int(
            min(
                max(
                    design["motor_KV"],
                    80
                ),
                1000
            )
        )

    if "wind_tolerance" in design:

        design["wind_tolerance"] = min(
            max(
                design["wind_tolerance"],
                5
            ),
            30
        )

    return design


def mutate_design(
        design
):

    d = copy.deepcopy(
        design
    )

    # Aerodynamics
    if "wing_area_m2" in d:

        d["wing_area_m2"] *= random.uniform(
            0.5,
            1.8
        )

    if "drag_coefficient" in d:
        d["drag_coefficient"] *= random.uniform(
            0.8,
            1.2
        )

    if "propeller_diameter_inch" in d:

        d["propeller_diameter_inch"] *= random.uniform(
            0.6,
            1.5
        )

    # Structures
    if "estimated_weight_kg" in d:

        d["estimated_weight_kg"] *= random.uniform(
            0.7,
            1.4
        )

    # Propulsion
    if "battery_mAh" in d:

        d["battery_mAh"] *= random.uniform(
            0.7,
            1.5
        )

    if "motor_KV" in d:

        d["motor_KV"] *= random.uniform(
            0.7,
            1.4
        )

    # Controls
    if "wind_tolerance" in d:

        d["wind_tolerance"] *= random.uniform(
            0.8,
            1.3
        )

    return d


def generate_variations(
        base_design,
        mission,
        n=1000
):

    designs = []

    for _ in range(n):

        d = mutate_design(
            base_design
        )

        d = enforce_constraints(
            d,
            mission
        )

        designs.append(
            d
        )

    return designs


# -------------------------
# Active Learning Support
# -------------------------

def generate_from_best(
        best_design,
        mission,
        n=500
):

    designs = []

    for _ in range(n):

        d = mutate_design(
            best_design
        )

        d = enforce_constraints(
            d,
            mission
        )

        designs.append(
            d
        )

    return designs