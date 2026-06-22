import json

from report_generator import (
    generate_top3_reports,
    save_reports
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
        "ranked_designs.json",
        "r"
) as f:

    ranked_designs = json.load(f)

reports = generate_top3_reports(
    ranked_designs,
    mission
)

save_reports(
    reports
)

print("\nTOP REPORT\n")

print(
    json.dumps(
        reports[0],
        indent=4
    )
)