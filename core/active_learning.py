from generator import (
    generate_variations
)

from ranker import (
    rank_designs,
    surrogate_score
)


def active_learning_loop(
        base_design,
        mission,
        rounds=3
):

    current_design = base_design

    best_designs = []

    history_metrics = []

    for round_num in range(rounds):

        print(
            f"\n===== ROUND {round_num + 1} ====="
        )

        candidates = generate_variations(
            current_design,
            mission,
            n=1000
        )

        ranked = rank_designs(
            candidates,
            mission
        )

        if len(ranked) == 0:

            print(
                "No valid designs found."
            )

            break

        best_design = ranked[0]

        best_designs.append(
            best_design
        )

        current_design = best_design

        top_designs = ranked[:10]

        avg_score = sum(
            surrogate_score(
                d,
                mission
            )
            for d in top_designs
        ) / len(top_designs)

        history_metrics.append(
            avg_score
        )

        print(
            f"Round {round_num + 1} Average Score: "
            f"{avg_score:.2f}"
        )

    improvement = 0

    if len(history_metrics) >= 2:

        improvement = (
            (
                history_metrics[-1]
                - history_metrics[0]
            )
            / history_metrics[0]
        ) * 100

    return {
        "best_designs": best_designs,
        "round_scores": history_metrics,
        "improvement_percent": round(
            improvement,
            2
        )
    }