AIR_DENSITY = 1.225
GRAVITY = 9.81


# ----------------------------
# Basic Aerodynamics
# ----------------------------

def calculate_lift(design):

    velocity = 20
    cl = 1.0

    return (
        0.5
        * AIR_DENSITY
        * velocity**2
        * design["wing_area_m2"]
        * cl
    )


def calculate_drag(design):

    velocity = 20

    return (
        0.5
        * AIR_DENSITY
        * velocity**2
        * design["wing_area_m2"]
        * design["drag_coefficient"]
    )


# ----------------------------
# Surrogate Models
# Requirement #4
# ----------------------------

def estimate_flight_time(design):

    battery_mAh = float(
        str(design.get("battery_mAh", 10000))
        .replace("mAh", "")
        .replace(",", "")
    )

    weight = design["estimated_weight_kg"]

    return battery_mAh / (weight * 1000)


def estimate_energy_consumption(design):

    weight = design["estimated_weight_kg"]

    return weight * 120


def estimate_structural_stress(design, mission):

    payload_force = (
        mission["payload_kg"]
        * GRAVITY
    )

    area = max(
        design["wing_area_m2"],
        0.1
    )

    return payload_force / area


def estimate_control_stability(design, mission):

    wind = mission["crosswind_m_s"]

    tolerance = design.get(
        "wind_tolerance",
        10
    )

    return tolerance / wind


def estimate_cost(design):

    battery_cost = (
        float(
            str(design.get("battery_mAh", 10000))
            .replace("mAh", "")
            .replace(",", "")
        )
        / 10
    )

    frame_cost = (
        design["estimated_weight_kg"]
        * 200
    )

    return battery_cost + frame_cost


# ----------------------------
# Validation
# ----------------------------

def can_fly(design):

    lift = calculate_lift(design)

    weight_force = (
        design["estimated_weight_kg"]
        * GRAVITY
    )

    return lift >= weight_force


def range_ok(design, mission):

    flight_time = estimate_flight_time(
        design
    )

    estimated_range = (
        flight_time * 40
    )

    return (
        estimated_range
        >= mission["range_km"]
    )


def wind_ok(design, mission):

    return (
        design.get(
            "wind_tolerance",
            0
        )
        >= mission["crosswind_m_s"]
    )


def budget_ok(design, mission):

    return (
        estimate_cost(design)
        <= mission["budget_usd"]
    )


def validate_design(
        design,
        mission
):

    return True