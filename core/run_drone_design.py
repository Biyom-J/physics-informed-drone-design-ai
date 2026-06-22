import json

from generator import generate_variations
from ranker import rank_designs

from report_generator import (
    generate_top3_reports,
    save_reports
)


def main():

    mission = {
        "payload_kg": 5,
        "range_km": 10,
        "crosswind_m_s": 15,
        "environment": "dense urban",
        "gps_available": False,
        "budget_usd": 5000,
        "single_drone": True
    }

    print("\nLoading Base Design...")

    with open(
            "base_design.json",
            "r"
    ) as f:

        base_design = json.load(f)

    print(
        "Generating Designs..."
    )

    designs = generate_variations(
        base_design,
        mission,
        n=1000
    )

    print(
        f"{len(designs)} designs generated."
    )

    print(
        "\nRanking Designs..."
    )

    ranked = rank_designs(
        designs,
        mission
    )

    with open(
            "ranked_designs.json",
            "w"
    ) as f:

        json.dump(
            ranked,
            f,
            indent=4
        )

    print(
        f"{len(ranked)} designs ranked."
    )

    print(
        "\nGenerating Reports..."
    )

    reports = generate_top3_reports(
        ranked,
        mission
    )

    save_reports(
        reports
    )

    print(
        "\nTop Design:"
    )

    print(
        json.dumps(
            ranked[0],
            indent=4
        )
    )

    print(
        "\nCompleted Successfully."
    )


if __name__ == "__main__":
    main()