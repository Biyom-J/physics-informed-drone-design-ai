import json

from active_learning import (
    active_learning_loop
)

mission = {
    "payload_kg": 5,
    "range_km": 10,
    "crosswind_m_s": 15,
    "environment": "dense urban",
    "gps_available": False,
    "budget_usd": 5000,
    "single_drone": True
}

with open(
        "base_design.json",
        "r"
) as f:

    base_design = json.load(f)

history = active_learning_loop(
    base_design,
    mission,
    rounds=3
)

print("\nFINAL BEST DESIGN\n")

print(history[-1])