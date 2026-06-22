import json

from generator import generate_variations
from ranker import rank_designs

mission = {
    "payload_kg": 5,
    "range_km": 10,
    "crosswind_m_s": 15,
    "environment": "dense urban",
    "gps_available": False,
    "budget_usd": 5000,
    "single_drone": True
}

with open("base_design.json", "r") as f:
    base_design = json.load(f)

designs = generate_variations(
    base_design,
    mission,
    n=1000
)

ranked = rank_designs(
    designs,
    mission
)

with open("ranked_designs.json", "w") as f:
    json.dump(
        ranked,
        f,
        indent=4
    )

print(
    f"Saved {len(ranked)} ranked designs."
)

print(
    "\nTop Design:\n"
)

print(
    json.dumps(
        ranked[0],
        indent=4
    )
)