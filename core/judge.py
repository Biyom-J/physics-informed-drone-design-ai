from physics import (
    estimate_flight_time,
    estimate_energy_consumption,
    estimate_control_stability,
    estimate_cost
)


def judge_design(
        design,
        mission
):

    flight_time = estimate_flight_time(
        design
    )

    energy = estimate_energy_consumption(
        design
    )

    stability = estimate_control_stability(
        design,
        mission
    )

    cost = estimate_cost(
        design
    )

    payload_score = mission[
        "payload_kg"
    ] * 10

    score = 0

    score += flight_time * 10
    score += stability * 20
    score += payload_score

    score -= energy * 0.05
    score -= cost * 0.01

    return score