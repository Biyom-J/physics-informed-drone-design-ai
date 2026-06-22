import json

from typing import TypedDict
from langgraph.graph import StateGraph, END

from agents import (
    aerodynamics_agent,
    propulsion_agent,
    structures_agent,
    control_agent
)

from supervisor import (
    clean_json,
    combine_agents
)

from ranker import rank_designs


# --------------------------------
# State
# --------------------------------

class DroneState(TypedDict):

    mission: dict

    aero: list
    prop: list
    struct: list
    control: list

    designs: list


# --------------------------------
# Agent Nodes
# --------------------------------

def aero_node(state):

    print(
        "\nRunning Aerodynamics Agent..."
    )

    result = aerodynamics_agent(
        state["mission"]
    )

    state["aero"] = clean_json(
        result
    )

    print(
        f"Generated {len(state['aero'])} aerodynamic proposals"
    )

    return state


def prop_node(state):

    print(
        "\nRunning Propulsion Agent..."
    )

    result = propulsion_agent(
        state["mission"]
    )

    state["prop"] = clean_json(
        result
    )

    print(
        f"Generated {len(state['prop'])} propulsion proposals"
    )

    return state


def struct_node(state):

    print(
        "\nRunning Structures Agent..."
    )

    result = structures_agent(
        state["mission"]
    )

    state["struct"] = clean_json(
        result
    )

    print(
        f"Generated {len(state['struct'])} structural proposals"
    )

    return state


def control_node(state):

    print(
        "\nRunning Control Agent..."
    )

    result = control_agent(
        state["mission"]
    )

    state["control"] = clean_json(
        result
    )

    print(
        f"Generated {len(state['control'])} control proposals"
    )

    return state


# --------------------------------
# Supervisor
# --------------------------------

def supervisor_node(state):

    print(
        "\nCombining Agent Outputs..."
    )

    designs = combine_agents(
        json.dumps(
            state["aero"]
        ),
        json.dumps(
            state["prop"]
        ),
        json.dumps(
            state["struct"]
        ),
        json.dumps(
            state["control"]
        ),
        num_designs=200
    )

    print(
        f"Generated {len(designs)} complete drone configurations"
    )

    state["designs"] = designs

    return state


# --------------------------------
# Judge
# --------------------------------

def judge_node(state):

    print(
        "\nML Screening + Physics Validation..."
    )

    ranked = rank_designs(
        state["designs"],
        state["mission"]
    )

    print(
        f"Final ranked designs: {len(ranked)}"
    )

    state["designs"] = ranked

    return state


# --------------------------------
# Build Graph
# --------------------------------

builder = StateGraph(
    DroneState
)

builder.add_node(
    "aero",
    aero_node
)

builder.add_node(
    "prop",
    prop_node
)

builder.add_node(
    "struct",
    struct_node
)

builder.add_node(
    "control",
    control_node
)

builder.add_node(
    "supervisor",
    supervisor_node
)

builder.add_node(
    "judge",
    judge_node
)

builder.set_entry_point(
    "aero"
)

builder.add_edge(
    "aero",
    "prop"
)

builder.add_edge(
    "prop",
    "struct"
)

builder.add_edge(
    "struct",
    "control"
)

builder.add_edge(
    "control",
    "supervisor"
)

builder.add_edge(
    "supervisor",
    "judge"
)

builder.add_edge(
    "judge",
    END
)

graph = builder.compile()


# --------------------------------
# Run
# --------------------------------

if __name__ == "__main__":

    mission = {

        "payload_kg": 5,
        "range_km": 10,
        "crosswind_m_s": 15,

        "environment": "dense urban",

        "gps_available": False,

        "budget_usd": 5000,

        "single_drone": True
    }

    result = graph.invoke(
        {
            "mission": mission
        }
    )

    print(
        "\nTOP 3 DESIGNS\n"
    )

    print(
        json.dumps(
            result["designs"][:3],
            indent=4
        )
    )