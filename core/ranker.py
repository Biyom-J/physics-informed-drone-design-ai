from physics import (
    validate_design,
    estimate_flight_time,
    estimate_energy_consumption,
    estimate_structural_stress,
    estimate_control_stability,
    estimate_cost
)

from ml_screener import (
    train_screener,
    predict_flight_time
)


def final_score(
        design,
        mission
):

    flight_time = estimate_flight_time(
        design
    )

    energy = estimate_energy_consumption(
        design
    )

    stress = estimate_structural_stress(
        design,
        mission
    )

    stability = estimate_control_stability(
        design,
        mission
    )

    cost = estimate_cost(
        design
    )

    score = 0

    score += flight_time * 10
    score += stability * 20

    score -= stress * 0.1
    score -= energy * 0.05
    score -= cost * 0.01

    return score


def design_distance(
        d1,
        d2
):

    return (

        abs(
            d1.get(
                "wing_area_m2",
                0
            )
            -
            d2.get(
                "wing_area_m2",
                0
            )
        )

        +

        abs(
            d1.get(
                "drag_coefficient",
                0
            )
            -
            d2.get(
                "drag_coefficient",
                0
            )
        )

        +

        abs(
            d1.get(
                "estimated_weight_kg",
                0
            )
            -
            d2.get(
                "estimated_weight_kg",
                0
            )
        )
    )


def rank_designs(
        designs,
        mission
):

    # ------------------
    # Stage 1
    # ML Screening
    # ------------------

    model = train_screener(
        designs
    )

    screened = sorted(
        designs,
        key=lambda d:
        predict_flight_time(
            model,
            d
        ),
        reverse=True
    )

    top20 = screened[:20]

    print(
        f"Top 20 selected from {len(designs)} designs"
    )

    # ------------------
    # Stage 2
    # Physics Validation
    # ------------------

    valid_designs = []

    for design in top20:

        if validate_design(
                design,
                mission
        ):

            valid_designs.append(
                design
            )

    print(
        f"Valid designs: {len(valid_designs)}"
    )

    # ------------------
    # Stage 3
    # High Fidelity Score
    # ------------------

    ranked = sorted(
        valid_designs,
        key=lambda d:
        final_score(
            d,
            mission
        ),
        reverse=True
    )

    # ------------------
    # Stage 4
    # Diversity Filter
    # ------------------

    diverse_designs = []

    for design in ranked:

        if len(
                diverse_designs
        ) == 0:

            diverse_designs.append(
                design
            )

            continue

        keep = True

        for existing in diverse_designs:

            distance = design_distance(
                design,
                existing
            )

            print("Distance:", distance)

            if distance < 0.05:
                keep = False
                break
        if keep:

            diverse_designs.append(
                design
            )

        if len(
                diverse_designs
        ) >= 20:

            break

    print(
        f"Diverse designs: {len(diverse_designs)}"
    )

    return diverse_designs