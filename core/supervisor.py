import json
import random


def clean_json(text):

    text = text.replace("```json", "")
    text = text.replace("```", "")

    return json.loads(text)


def combine_agents(
        aero,
        prop,
        struct,
        control,
        num_designs=200
):

    aero = clean_json(aero)
    prop = clean_json(prop)
    struct = clean_json(struct)
    control = clean_json(control)

    complete_designs = []

    for _ in range(num_designs):

        design = {}

        design.update(
            random.choice(aero)
        )

        design.update(
            random.choice(prop)
        )

        design.update(
            random.choice(struct)
        )

        design.update(
            random.choice(control)
        )

        complete_designs.append(
            design
        )

    return complete_designs


def extract_design(design):

    clean = {}

    # Aerodynamics
    for key in [
        "wing_area_m2",
        "drag_coefficient",
        "propeller_diameter_inch",
        "fuselage_design"
    ]:
        if key in design:
            clean[key] = design[key]

    # Propulsion
    for key in [
        "battery_mAh",
        "motor_KV",
        "motor_type",
        "voltage"
    ]:
        if key in design:
            clean[key] = design[key]

    # Structures
    for key in [
        "material",
        "estimated_weight_kg",
        "safety_factor",
        "estimated_cost_usd"
    ]:
        if key in design:
            clean[key] = design[key]

    # Control
    for key in [
        "kp",
        "ki",
        "kd",
        "wind_tolerance",
        "navigation_method"
    ]:
        if key in design:
            clean[key] = design[key]

    return clean