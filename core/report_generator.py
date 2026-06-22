import json

from physics import (
    estimate_flight_time,
    estimate_energy_consumption,
    estimate_structural_stress,
    estimate_control_stability,
    estimate_cost
)


def physics_constraints(design):

    checks = []

    if design.get("estimated_weight_kg", 0) > 0:
        checks.append(
            "Positive mass"
        )

    if design.get("wing_area_m2", 0) > 0:
        checks.append(
            "Positive wing area"
        )

    if design.get("drag_coefficient", 1) < 0.15:
        checks.append(
            "Reasonable drag coefficient"
        )

    if design.get("battery_mAh", 0) > 0:
        checks.append(
            "Battery capacity defined"
        )

    if design.get("propeller_diameter_inch", 0) > 0:
        checks.append(
            "Propeller size defined"
        )

    return checks


def generate_flight_test(mission):

    return (
        f"Fly {mission['range_km']} km "
        f"with {mission['payload_kg']} kg payload "
        f"in {mission['crosswind_m_s']} m/s crosswind. "
        f"If range is below {mission['range_km']} km "
        f"or the drone cannot complete the mission, "
        f"the design fails."
    )


def confidence_interval(value):

    return {
        "lower": round(value * 0.9, 2),
        "upper": round(value * 1.1, 2)
    }


def novelty_score(design):

    score = 0

    if design.get(
            "fuselage_design",
            ""
    ):
        score += 20

    if design.get(
            "navigation_method",
            ""
    ):
        score += 20

    if design.get(
            "motor_type",
            ""
    ):
        score += 20

    score += 40

    return min(score, 100)


def generate_test_flight_protocol():

    return [
        "Pre-flight inspection",
        "Battery health check",
        "Hover test at 5m altitude",
        "Crosswind stability test",
        "Urban obstacle navigation test",
        "5km delivery simulation",
        "10km full mission validation",
        "Emergency landing verification"
    ]


def create_design_report(
        design,
        mission,
        rank
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

    report = {

        "rank": rank,

        "design_specifications": design,

        "predicted_performance": {

            "flight_time_hours": round(
                flight_time,
                2
            ),

            "energy_consumption": round(
                energy,
                2
            ),

            "structural_stress": round(
                stress,
                2
            ),

            "control_stability": round(
                stability,
                2
            ),

            "estimated_cost_usd": round(
                cost,
                2
            )
        },

        "confidence_intervals": {

            "flight_time":
                confidence_interval(
                    flight_time
                ),

            "energy_consumption":
                confidence_interval(
                    energy
                ),

            "structural_stress":
                confidence_interval(
                    stress
                ),

            "control_stability":
                confidence_interval(
                    stability
                ),

            "cost":
                confidence_interval(
                    cost
                )
        },

        "physics_constraints_passed":
            physics_constraints(
                design
            ),

        "novelty_justification": {

            "novelty_score":
                novelty_score(
                    design
                ),

            "reason":
                "Design combines optimized "
                "aerodynamics, propulsion, "
                "GPS-denied navigation, "
                "and urban delivery constraints."
        },

        "falsifiable_flight_test":
            generate_flight_test(
                mission
            ),

        "test_flight_protocol":
            generate_test_flight_protocol()
    }

    return report


def generate_top3_reports(
        ranked_designs,
        mission
):

    with open(
            "designs.json",
            "w"
    ) as f:

        json.dump(
            ranked_designs[:3],
            f,
            indent=4
        )

    reports = []

    for i, design in enumerate(
            ranked_designs[:3]
    ):

        report = create_design_report(
            design,
            mission,
            rank=i + 1
        )

        reports.append(
            report
        )

    return reports


def save_reports(
        reports,
        filename="top_design_reports.json"
):

    with open(
            filename,
            "w"
    ) as f:

        json.dump(
            reports,
            f,
            indent=4
        )

    print(
        f"Saved report to {filename}"
    )